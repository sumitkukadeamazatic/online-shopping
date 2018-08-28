from rest_framework import serializers
from order.models import Cart, CartProduct
from product.models import Product, ProductSeller


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model  = Product
        fields = ('slug', 'name', 'selling_price', 'images')
    

class ProductSellerSerializers(serializers.ModelSerializer):
    product = ProductSerializers(read_only=True)
    class Meta: 
        model = ProductSeller
        fields = ('quantity','product')


class CartSerializer(serializers.ModelSerializer):
    product_seller = ProductSellerSerializers(read_only=True)
    class Meta:
        model = CartProduct
        fields = ('quantity','product_seller')