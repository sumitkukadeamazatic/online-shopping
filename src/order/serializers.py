from rest_framework import serializers
from order.models import Cart, CartProduct, Order, OrderLog, Lineitem, LineitemTax
from product.models import CategoryTax
  

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
    
    def validate_quantity(self, value):
        if value<0:
            raise serializers.ValidationError("quantity not less than 0")
        return value
    
    

class AddCartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ('quantity', 'product_seller')
    
    def validate_quantity(self, value):
        if value<=0:
            raise serializers.ValidationError("quantity not less than 0")
        return value
    
    def create(self, obj):
        user = self.context['request'].user
        cart=Cart.objects.get_or_create(user=user,is_cart_processed=False)[0]
        return CartProduct.objects.create(cart=cart, quantity = obj['quantity'], product_seller = obj['product_seller'], is_order_generated = False)

class OrderSerializer(serializers.ModelSerializer):
    order_place_date = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    shipping_address = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'order_place_date', 'total_price','shipping_address','products')
    
    def get_order_place_date(self, obj):
        return OrderLog.objects.get(lineitem=Lineitem.objects.get(order=obj),status='place-order').created_at.date()
    
    def get_total_price(self, obj):
        lis = Lineitem.objects.filter(order=obj)
        tprice = 0
        for li in lis:
            tprice += ((li.selling_price - li.selling_price* li.discount/100) + li.gift_wrap_charges) * li.quantity 
        return tprice + obj.totoal_shipping_cost

    def get_shipping_address(self, obj):
        return {
                'name' : obj.shipping_name,
                'address_line' : obj.shipping_address_line,
                'pincode' : obj.shipping_pincode,
                'phone_number' : obj.shiping_contact_no
            }
        
    def get_products(self, obj): 
        lis = Lineitem.objects.filter(order=obj)
        data = []
        for li in lis:
            data.append(
                {
                    "product_name" : li.product.name,
                    "price" : li.selling_price,
                    "img" : li.product.images
                }
            )
        return data

class TaxSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = CategoryTax
        fields = ('name', 'percentage')
    def get_name(self, obj):
        return obj.tax.name

class TaxInvoiceSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    tax_type = serializers.SerializerMethodField()
    tax_rate = serializers.SerializerMethodField()

    class Meta:
        model = Lineitem
        fields = ('product_name', 'quantity', 'selling_price', 'tax_type', 'tax_rate')

    def get_product_name(self, obj):
        return obj.product.name
    def get_tax_type(self, obj):
        return LineitemTax.objects.filter(lineitem=obj).tax_name
    def get_tax_rate(self, obj):
        return LineitemTax.objects.filter(lineitem=obj).tax_amount

