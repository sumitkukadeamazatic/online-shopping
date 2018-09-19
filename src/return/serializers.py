"""
Return App serializers
"""

from rest_framework import serializers
from .models import Lineitem, LineitemShippingDetail
from order.models import ShippingDetails


class ShippingDetailsSerializer(serializers.ModelSerializer):
    """
    Model serializer for shipping details
    """

    class Meta:
        model = ShippingDetails
        exclude = ('created_at', 'updated_at')


class ReturnLineItemSerializer(serializers.ModelSerializer):
    """
    Model serializer for Return Line Items
    """

    class Meta:
        model = Lineitem
        exclude = ('created_at', 'updated_at')


class ReturnLineitemShippingSerializer(serializers.ModelSerializer):
    """
    Model serializer for return line item shipping details
    """

    class Meta:
        model = LineitemShippingDetail
        exclude = ('created_at', 'updated_at')
