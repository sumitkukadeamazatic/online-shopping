from rest_framework import serializers
from order.models import Cart, CartProduct
  

class CartProductSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    price =serializers.SerializerMethodField()
    img = serializers.SerializerMethodField()
    in_stock = serializers.SerializerMethodField()

    class Meta:
        model = CartProduct
        fields = ('id', 'slug', 'name', 'price', 'in_stock', 'quantity', 'img')
   
    def get_slug(self,obj):
        return obj.product_seller.product.slug

    def get_name(self,obj):
        return obj.product_seller.product.name

    def get_price(self,obj):
        return obj.product_seller.product.selling_price

    def get_img(self,obj):
        return obj.product_seller.product.images 
        
    def get_in_stock(self,obj):
        return obj.product_seller.quantity>0

class CartProductPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ('id','quantity', 'product_seller', 'is_order_generated', 'cart')