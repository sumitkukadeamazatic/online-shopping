"""
Offer App serializers
"""

from datetime import datetime
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from utils import serializers as utils_serializers
from .models import Offer, UserOffer, ProductOffer


class OfferSerializer(serializers.ModelSerializer):
    """
    Offer model serializer
    """

    class Meta:
        model = Offer
        exclude = ('created_at', 'updated_at')


class OfferValidateSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Serializer used for validating an offer
    """

    user_id = serializers.IntegerField(required=False, default=None)
    code = serializers.CharField()
    product = utils_serializers.IntegerListField(required=False, default=[])
    total_order_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2)

    def validate(self, data):       # pylint: disable=arguments-differ
        today = timezone.localdate()
        offer = Offer.objects.filter(
            code=data['code'], valid_from__lte=today, valid_upto__gte=today).first()
        if offer is None:
            raise ParseError(detail='Invalid coupon code.')

        # First check is this offer assigned to users exclusively
        user_offer_relations = UserOffer.objects.filter(offer=offer)
        if user_offer_relations:
            user_offer = user_offer_relations.filter(
                user__id=data['user_id'], is_redeemed=False).first()
            if user_offer is None:
                raise ParseError(detail='Invalid data.')

        # Check if offer is assigned to some specific products
        product_offer_relation = ProductOffer.objects.filter(offers=offer)
        if product_offer_relation:
            product_offer = product_offer_relation.filter(
                product_id__in=data['product'])
            if not product_offer:
                raise ParseError(detail='Invalid data.')

        # Check if offer has time limitation (e.g. offer is valid in 1PM-4PM)
        if not ((offer.start_time is None) and (offer.end_time is None)):
            time = datetime.time(datetime.now())
            if not offer.start_time <= time <= offer.end_time:
                raise ParseError(detail='Invalid data.')

        # Check if offer has weekday limitation (e.g. offer is valid only on Mondays)
        if offer.days:
            weekday = (datetime.today()).weekday()
            if not weekday in offer.days:
                raise ParseError(detail='Invalid data.')

        # Check if offer has minimum order amount restriction
        if not offer is None:
            if data['total_order_amount'] < offer.minimum:
                raise ParseError(detail='Invalid data.')

        # Offer has either a fixed amount to deduct or a percentage
        if not offer.amount is None:
            discounted_amount = data['total_order_amount'] - offer.amount
        elif not offer.percentage is None:
            discount = data['total_order_amount'] - (offer.percentage / 100)
            # Offer might have maximum discount amount limit
            if (not offer.amount_limit is None) and discount > offer.amount_limit:
                discount = offer.amount_limit
            discounted_amount = data['total_order_amount'] - discount
        else:
            raise ParseError(detail='Invalid data.')
        validated_data = {
            'offer_id': offer.id,
            'discounted_amount': discounted_amount
        }
        return validated_data
