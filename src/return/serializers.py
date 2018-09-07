from rest_framework import serializers
from .models import Order, Lineitem

class ReturnSerializer(serializers.ModelSerializer):
    """
        Return Serializer
    """

    class Meta:
        model = Order
        fields = (
            'id',
            'created_at',
            'updated_at',
            'status',
            'order',
        )


class ReturnLineitemSerializer(serializers.ModelSerializer):
    """
        Return Lineitem Serializer
    """

    class Meta:
        model = Lineitem
        fields = (
            'quantity',
            'reason',
            'description',
            'status',
            'lineitem',
            'return_order',
        )

    def create(self, validated_data):
        print (validated_data)
        return 
