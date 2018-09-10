"""
Offer App serializers
"""

from rest_framework.serializers import ModelSerializer
from .models import Offer


class OfferSerializer(ModelSerializer):
    """
    Offer model serializer
    """

    class Meta:
        model = Offer
        exclude = ('created_at', 'updated_at')
