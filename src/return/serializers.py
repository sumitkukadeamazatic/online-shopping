"""
Return App serializers
"""
from rest_framework import serializers
from order.models import ShippingDetails
from .models import Order as ReturnOrder, Lineitem as ReturnLineitem, OrderLog as ReturnOrderLog, LineitemShippingDetail as ReturnLineitemShippingDetail


class ReturnOrderSerializer(serializers.ModelSerializer):
    """
    Model serializer for model return_order
    """

    class Meta:
        model = ReturnOrder
        exclude = ('created_at', 'updated_at')

    def create(self, validated_data):
        return ReturnOrder.objects.create(status=ReturnOrder.GENERATED, order=validated_data['order'])


class ReturnOrderLogSerializer(serializers.ModelSerializer):
    """
    Model Serializer for model return order logs
    """

    class Meta:
        model = ReturnOrderLog
        exclude = ('created_at', 'updated_at')

    def create(self, validated_data):
        return ReturnOrderLog.objects.create(**validated_data)


class ReturnLineitemSerializer(serializers.ModelSerializer):
    """
    Model serializer for model return_order
    """

    class Meta:
        model = ReturnLineitem
        exclude = ('created_at', 'updated_at')
        extra_kwargs = {
            'status': {
                'required': False
            },
            'return_order': {
                'required': False
            }
        }

    def create(self, validated_data):
        return_order = ReturnOrder.objects.filter(
            order=validated_data['lineitem'].order).first()
        if return_order is None:
            return_order_serializer = ReturnOrderSerializer(
                data={'order': validated_data['lineitem'].order.id})
            return_order_serializer.is_valid(raise_exception=True)
            return_order = return_order_serializer.save()
        validated_data.update({
            'return_order': return_order,
            'status': ReturnLineitem.GENERATED
        })
        return_lineitem = ReturnLineitem.objects.create(**validated_data)
        log_data = {
            'return_lineitem': return_lineitem.id,
            'status': ReturnLineitem.GENERATED
        }
        log_serializer = ReturnOrderLogSerializer(data=log_data)
        log_serializer.is_valid(raise_exception=True)
        log_serializer.save()
        response_data = {
            'message': 'Return order created successfully'
        }
        return response_data


class ShippingDetailsSerializer(serializers.ModelSerializer):
    """
    Model serializer for shipping details
    """

    class Meta:
        model = ShippingDetails
        exclude = ('created_at', 'updated_at')


class PartialReturnLineitemSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Serializer for Return Line Items
    """

    quantity = serializers.IntegerField()
    description = serializers.CharField(required=False, allow_blank=True)
    return_lineitem = serializers.PrimaryKeyRelatedField(
        queryset=ReturnLineitem.objects.all())


class ReturnLineitemShippingSerializer(serializers.Serializer):  # pylint: disable=abstract-method
    """
    Serializer for return line item shipping details
    """
    shipping_details = ShippingDetailsSerializer()
    lineitems = PartialReturnLineitemSerializer(many=True)

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


class ViewReturnLineitemSerializer(serializers.ModelSerializer):
    """
    Serializer to view ReturnLineitem
    """

    product_name = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_product_name(self, obj):  # pylint: disable=no-self-use
        """
        Method to get product name from lineitem to product relation
        """
        return ReturnLineitem.objects.filter(id=obj['id']).values('lineitem__product_seller__product__name').first()['lineitem__product_seller__product__name']
        # return obj.lineitem.product_seller.product.name

    def get_price(self, obj):  # pylint: disable=no-self-use
        """
        Method to get selling price of lineitem
        """
        return ReturnLineitem.objects.filter(id=obj['id']).values('lineitem__selling_price').first()['lineitem__selling_price']
        # return obj.lineitem.selling_price

    def get_image(self, obj):  # pylint: disable=no-self-use
        """
        Method to get product images from lineitem to product relation
        """
        return ReturnLineitem.objects.filter(id=obj['id']).values('lineitem__product_seller__product__images').first()['lineitem__product_seller__product__images']
        # return obj.lineitem.product_seller.product.images

    class Meta:
        model = ReturnLineitem
        fields = (
            'id',
            'product_name',
            'price',
            'image',
            'status',
            'quantity',
            'reason',
            'description'
        )
        extra_kwargs = {
            'id': {
                'read_only': False
            }
        }


class ViewReturnSerializer(serializers.ModelSerializer):
    """
        Serializer to view ReturnOrder
    """
    order_id = serializers.IntegerField()
    lineitems = serializers.SerializerMethodField()

    class Meta:
        model = ReturnOrder
        fields = (
            'id',
            'status',
            'created_at',
            'order_id',
            'lineitems',
        )
        extra_kwargs = {
            'id': {
                'read_only': False,
            },
            'created_at': {
                'read_only': False
            },
        }

    def get_lineitems(self, obj):  # pylint: disable=no-self-use
        """
        Method to get lineitems data using serializer
        """
        lineitems_data = ReturnLineitem.objects.filter(
            return_order_id=obj['id']).values()
        lineitem_serializer = ViewReturnLineitemSerializer(
            data=list(lineitems_data), many=True)
        lineitem_serializer.is_valid(raise_exception=True)
        return lineitem_serializer.data
