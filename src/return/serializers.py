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


class ReturnLineItemSerializer(serializers.Serializer):
    """
    Serializer for Return Line Items
    """

    quantity = serializers.IntegerField()
    description = serializers.CharField(required=False, allow_blank=True)
    return_lineitem = serializers.PrimaryKeyRelatedField(
        queryset=Lineitem.objects.all())


class ReturnLineitemShippingSerializer(serializers.Serializer):
    """
    Serializer for return line item shipping details
    """
    shipping_details = ShippingDetailsSerializer()
    lineitems = ReturnLineItemSerializer(many=True)

    class Meta:
        model = LineitemShippingDetail
        fields = ('shipping_details', 'lineitems')

    def create(self, validated_data):
        # shipping_details_data = validated_data['shipping_details']
        # shipping_detail = ShippingDetails.objects.create(
        #     **shipping_details_data)
        # lineitems = validated_data['lineitems']
        # for lineitem in lineitems:
        #     lineitem.update({'shipping_detail': shipping_detail})
        #     LineitemShippingDetail.objects.create(**lineitem)
        validated_data.update({
            'message': 'Lineitem shipping details created successfully'})
        print(validated_data, '########################################')
        return validated_data
