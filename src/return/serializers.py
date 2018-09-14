from rest_framework import serializers
from .models import Order as ReturnOrder, Lineitem as ReturnLineitem, OrderLog as ReturnOrderLog
from order.models import Order, Lineitem

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

class ReturnLineitemSerializer(serializers.ModelSerializer):
    """
        ReturnLineitem Serializer
    """

    class Meta:
        model = ReturnLineitem
        fields = (
            'reason',
            'description',
        )

    def create(self, validated_data):
        print (self.context)
        print (validated_data)
        print (self.context['request'].data)
        if not ReturnOrder.objects.filter(order_id=self.context['order']):
            returnOrder_serializer = ReturnOrderSerializer(data=self.context)
            if returnOrder_serializer.is_valid():
                returnOrder_serializer.save()
        lineitem_data = Lineitem.objects.filter(order=self.context['order'], product=self.context['product']).values().first()  # order_lineitem
        return_order_id = ReturnOrder.objects.get(order=self.context['order'])
        returnLineitem_serializer = ReturnLineitem.objects.create(quantity=lineitem_data['quantity'], reason=validated_data['reason'], description=validated_data['description'], lineitem_id=lineitem_data['id'], return_order=return_order_id, status=lineitem_data['status'])
        returnOrderLog_data = {'status': returnLineitem_serializer.status,'description': returnLineitem_serializer.description,'return_lineitem': returnLineitem_serializer.id}
        returnOrderLog_serializer = ReturnOrderLogSerializer(data=returnOrderLog_data)
        if returnOrderLog_serializer.is_valid():
            returnOrderLog_serializer.save()
        return returnLineitem_serializer


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
        lineitem_data = Lineitem.objects.filter(order=content['order'], product=content['product']).values().first()
        return_order_id = ReturnOrder.objects.get(order=content['order'])
        returnLineitem_serializer = ReturnLineitem.objects.create(quantity=lineitem_data['quantity'], reason=validated_data['reason'], description=validated_data['description'], lineitem_id=lineitem_data['id'], return_order=return_order_id, status=lineitem_data['status'])
        returnOrderLog_data = {'status': returnLineitem_serializer.status,'description': returnLineitem_serializer.description,'return_lineitem': returnLineitem_serializer.id}
        returnOrderLog_serializer = ReturnOrderLogSerializer(data=returnOrderLog_data)
        if returnOrderLog_serializer.is_valid():
            returnOrderLog_serializer.save()
        return returnLineitem_serializer


class ViewReturnLineitemSerializer(serializers.ModelSerializer):
    """
        Serializer to view ReturnLineitem
    """

    return_lineitem_id = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()

    def get_return_lineitem_id(self, obj):
        return obj.id

    def get_status(self, obj):
        return obj.status

    def get_quantity(self, obj):
        return obj.quantity
   
    class Meta:
        model = ReturnLineitem
        fields=(
            'return_lineitem_id',
            'product_name',
            # 'price',
            # 'image',
            'status',
            'quantity',
        )

class ViewReturnSerializer(serializers.ModelSerializer):
    """
        Serializer to view ReturnOrder
    """
    '''
    return_lineitems = serializers.SerializerMethodField()

    def get_return_lineitems(self, obj):
        serialized_data = ViewReturnLineitemSerializer(obj.return_lineitems.all(), many=True, read_only=True, context=self.context)
        return serialized_data.data
    '''

    #image = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    return_lineitems = serializers.SerializerMethodField()

    def get_id(self, obj):
        print (obj.return_order.id)
        return 1

    def get_return_lineitems(self, obj):
        return (ViewReturnLineitemSerializer(obj).data)

    class Meta:
        model = ReturnOrder
        fields = (
            'id',
            'return_lineitems',
        )
