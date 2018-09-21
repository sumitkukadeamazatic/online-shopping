"""
Return App serializers
"""
from django.db.models import Q
from rest_framework import serializers
from order.models import ShippingDetails, Order, Lineitem
from product.models import Product
from .models import Order as ReturnOrder, Lineitem as ReturnLineitem, OrderLog as ReturnOrderLog, LineitemShippingDetail as ReturnLineitemShippingDetail


class ShippingDetailsSerializer(serializers.ModelSerializer):
    """
    Model serializer for shipping details
    """

    class Meta:
        model = ShippingDetails
        exclude = ('created_at', 'updated_at')


class ReturnLineitemSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Serializer for Return Line Items
    """

    quantity = serializers.IntegerField()
    description = serializers.CharField(required=False, allow_blank=True)
    return_lineitem = serializers.PrimaryKeyRelatedField(
        queryset=ReturnLineitem.objects.filter(~Q(id__in=(ReturnLineitemShippingDetail.objects.values_list('id', flat=True)))))


class ReturnLineitemShippingSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Serializer for return line item shipping details
    """
    shipping_details = ShippingDetailsSerializer()
    lineitems = ReturnLineitemSerializer(many=True)

    def create(self, validated_data):
        shipping_details_data = validated_data['shipping_details']
        shipping_detail = ShippingDetails.objects.create(
            **shipping_details_data)
        lineitems = validated_data['lineitems']
        for lineitem in lineitems:
            lineitem.update({'shipping_detail': shipping_detail})
            ReturnLineitemShippingDetail.objects.create(**lineitem)
        validated_data.update({
            'response': {
                'message': 'Lineitem shipping details created successfully'
            }
        })
        return validated_data


class ReturnOrderSerializer(serializers.ModelSerializer):
    """
        ReturnOrder Serializer
    """

    class Meta:
        model = ReturnOrder
        fields = (
            'order',
        )

    def create(self, validated_data):
        return ReturnOrder.objects.create(status=validated_data['order'].status, order_id=validated_data['order'].id)


class ReturnOrderLogSerializer(serializers.ModelSerializer):
    """
        ReturnOrderLog Serializer
    """

    class Meta:
        model = ReturnOrderLog
        fields = (
            'status',
            'description',
            'return_lineitem',
        )

# changes in order_lineitem (product_id, seller_id -> product_seller_id)


class ReturnSerializer(serializers.ModelSerializer):
    """
        Return Serializer
    """

    class Meta:
        model = ReturnLineitem
        fields = (
            'reason',
            'description',
        )

    def create(self, validated_data):
        content = self.context['request'].data
        if not ReturnOrder.objects.filter(order_id=content['order']):
            returnOrder_serializer = ReturnOrderSerializer(data=content)
            if returnOrder_serializer.is_valid():
                returnOrder_serializer.save()
        lineitem_data = Lineitem.objects.filter(
            order=content['order'], product=content['product']).values().first()
        return_order_id = ReturnOrder.objects.get(order=content['order'])
        returnLineitem_serializer = ReturnLineitem.objects.create(quantity=lineitem_data['quantity'], reason=validated_data['reason'], description=validated_data[
                                                                  'description'], lineitem_id=lineitem_data['id'], return_order=return_order_id, status=lineitem_data['status'])
        returnOrderLog_data = {'status': returnLineitem_serializer.status,
                               'description': returnLineitem_serializer.description, 'return_lineitem': returnLineitem_serializer.id}
        returnOrderLog_serializer = ReturnOrderLogSerializer(
            data=returnOrderLog_data)
        if returnOrderLog_serializer.is_valid():
            returnOrderLog_serializer.save()
        return returnLineitem_serializer


class ViewReturnLineitemSerializer(serializers.ModelSerializer):
    """
        Serializer to view ReturnLineitem
    """

    return_lineitem_id = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()

    def get_return_lineitem_id(self, obj):
        return obj.id

    def get_product_name(self, obj):
        return Product.objects.get(id=(Lineitem.objects.get(id=obj.lineitem_id).product_id)).name

    def get_price(self, obj):
        return Lineitem.objects.get(id=obj.lineitem_id).selling_price

    def get_image(self, obj):
        return Product.objects.get(id=(Lineitem.objects.get(id=obj.lineitem_id).product_id)).images

    def get_status(self, obj):
        return obj.status

    def get_quantity(self, obj):
        return obj.quantity

    class Meta:
        model = ReturnLineitem
        fields = (
            'return_lineitem_id',
            'product_name',
            'price',
            'image',
            'status',
            'quantity',
        )


class ViewReturnSerializer(serializers.ModelSerializer):
    """
        Serializer to view ReturnOrder
    """

    id = serializers.SerializerMethodField()
    return_lineitems = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.return_order_id

    def get_return_lineitems(self, obj):
        return (ViewReturnLineitemSerializer(obj).data)

    class Meta:
        model = ReturnOrder
        fields = (
            'id',
            'return_lineitems',
        )
