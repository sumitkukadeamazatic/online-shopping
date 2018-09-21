"""
Return App serializers
"""
from django.db.models import Q
from rest_framework import serializers
from order.models import ShippingDetails
from .models import Lineitem, LineitemShippingDetail


class ShippingDetailsSerializer(serializers.ModelSerializer):
    """
    Model serializer for shipping details
    """

    class Meta:
        model = ShippingDetails
        exclude = ('created_at', 'updated_at')


class ReturnLineItemSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Serializer for Return Line Items
    """

    quantity = serializers.IntegerField()
    description = serializers.CharField(required=False, allow_blank=True)
    return_lineitem = serializers.PrimaryKeyRelatedField(
        queryset=Lineitem.objects.filter(~Q(id__in=(LineitemShippingDetail.objects.values_list('id', flat=True)))))


class ReturnLineitemShippingSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Serializer for return line item shipping details
    """
    shipping_details = ShippingDetailsSerializer()
    lineitems = ReturnLineItemSerializer(many=True)

    def create(self, validated_data):
        shipping_details_data = validated_data['shipping_details']
        shipping_detail = ShippingDetails.objects.create(
            **shipping_details_data)
        lineitems = validated_data['lineitems']
        for lineitem in lineitems:
            lineitem.update({'shipping_detail': shipping_detail})
            LineitemShippingDetail.objects.create(**lineitem)
        validated_data.update({
            'response': {
                'message': 'Lineitem shipping details created successfully'
            }
        })
        return validated_data
