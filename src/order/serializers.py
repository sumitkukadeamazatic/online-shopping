from rest_framework import serializers
from order.models import Cart, CartProduct, Order, OrderLog, Lineitem, LineitemTax, PaymentMethod
from product.models import CategoryTax
from product.models import ProductSeller
from contact.models import Address
from offer.models import Offer, OrderOffer, OfferLineitem
import json

class CartProductSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    price =serializers.SerializerMethodField()
    img = serializers.SerializerMethodField()
    in_stock = serializers.SerializerMethodField()

    class Meta:
        model = CartProduct
        fields = ('id', 'slug', 'name', 'price', 'in_stock', 'quantity', 'img')
   
    def get_slug(self, obj):
        return obj.product_seller.product.slug

    def get_name(self, obj):
        return obj.product_seller.product.name

    def get_price(self, obj):
        return obj.product_seller.selling_price

    def get_img(self, obj):
        return obj.product_seller.product.images 
        
    def get_in_stock(self, obj):
        return obj.product_seller.quantity > 0

    def validate_quantity(self, value):
        if value<0:
            raise serializers.ValidationError("quantity not less than 0")
        return value

    def validate(self, data):
        if not ProductSeller.objects.filter(pk=self.context['request'].data['product_seller']):
            raise serializers.ValidationError("%s not valid product_seller id"%(self.context['request'].data['product_seller']))
        return data

    def create(self, obj):        
        cart=Cart.objects.get_or_create(user=self.context['request'].user, is_cart_processed=False)[0]
        product_seller = ProductSeller.objects.get(pk=self.context['request'].data['product_seller'])
        return CartProduct.objects.create(cart=cart, quantity = obj['quantity'], product_seller = product_seller, is_order_generated = self.context['request'].data['is_order_generated'])


def get_discount_amount(offer_ids, amount):
    offers = Offer.objects.filter(id__in=offer_ids).values_list('amount','percentage')
    for offer in offers:
            if offer[0]:
                amount -= offer[0]
            else:
                amount -= (amount*offer[1]/100) 
    return amount  

class OrderSerializer(serializers.ModelSerializer):
    order_place_date = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    shipping_address = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()
    

    class Meta:
        model = Order
        fields = ('id', 'order_place_date', 'total_price','shipping_address','products')
    
    def get_order_place_date(self, obj):
        return OrderLog.objects.get(lineitem=Lineitem.objects.get(order=obj)).created_at.date()
    
    def get_total_price(self, obj):
        offers = Offer.objects.filter(id__in=OrderOffer.objects.filter(order=obj).values_list('offer'))
        
        lis = Lineitem.objects.filter(order=obj)
        tprice = 0
        for li in lis:
            tprice += (get_discount_amount(Offer.objects.filter(id__in=OfferLineitem.objects.filter(lineitem=li).values_list('offer')), li.selling_price) + li.gift_wrap_charges) * li.quantity
        discoutPrice = tprice
        discoutPrice = get_discount_amount(offers, tprice)
        return discoutPrice + obj.totoal_shipping_cost

    def get_shipping_address(self, obj):
        return {
                'name' : obj.shipping_name,
                'address_line' : obj.shipping_address_line,
                'pincode' : obj.shipping_pincode,
                'phone_number' : obj.shipping_contact_no
            }
        
    def get_products(self, obj): 
        lis = Lineitem.objects.filter(order=obj)
        data = []
        for li in lis:
            data.append(
                {
                    "product_name" : li.product_seller.product.name,
                    "price" : li.selling_price,
                    "img" : li.product_seller.product.images
                }
            )
        return data

    def validate(self, data):
        if not Cart.objects.filter(pk=self.context['request'].data['cart']):
            raise serializers.ValidationError("%s is not a vaid Cart id"%(self.context['request'].data['cart']))

        if not Address.objects.filter(pk=self.context['request'].data['bill_address']):
            raise serializers.ValidationError("%s is not a vaid bill_address id"%(self.context['request'].data['bill_address']))

        if not Address.objects.filter(pk=self.context['request'].data['shipping_address']):
            raise serializers.ValidationError("%s is not a vaid shipping_address id"%(self.context['request'].data['shipping_address']))
        for offer in json.loads(self.context['request'].data['offers']):
            if not Offer.objects.filter(pk=offer):
                raise serializers.ValidationError("%s is not a vaid offer id"%(offer))

        if not PaymentMethod.objects.filter(pk=self.context['request'].data['payment_method']):
            raise serializers.ValidationError("%s is not a vaid payment_method id"%(self.context['request'].data['payment_method']))

        for product in json.loads(self.context['request'].data['products']):
            for offer in product['offers']:
                if not Offer.objects.filter(pk=offer):
                    raise serializers.ValidationError("%s is not a vaid offer id"%(offer))
            if not ProductSeller.objects.filter(pk=product['product_seller']):
                raise serializers.ValidationError("%s is not a vaid product_seller id"%(product['product_seller']))
        return data

    
    def create(self , validate_data):
        cart = Cart.objects.get(pk=self.context['request'].data['cart'])
        bill_address = Address.objects.get(pk=self.context['request'].data['bill_address'])
        shipping_address =Address.objects.get(pk=self.context['request'].data['shipping_address'])
        offers = Offer.objects.filter(id__in=json.loads(self.context['request'].data['offers']))
        payment_method = PaymentMethod.objects.get(pk=self.context['request'].data['payment_method'])
        products = json.loads(self.context['request'].data['products'])
        order = Order.objects.create(
            payment_method = payment_method,
            cart = cart,
            shipping_name = shipping_address.name,
            shipping_address_line = shipping_address.address_line,
            shipping_contact_no = shipping_address.contact_no,
            shipping_city = shipping_address.city,
            shipping_state = shipping_address.state,
            shipping_pincode = shipping_address.pincode,
            billing_name = bill_address.name,
            billing_address_line = bill_address.address_line,
            billing_city = bill_address.city,
            billing_state = bill_address.state,
            billing_pincode = bill_address.pincode,
            totoal_shipping_cost = sum([product['shipping_cost'] for product in products if 'shipping_cost' in product]),   
            status = 'order-genrated'
        )
       
        for offer in offers:
            OrderOffer.objects.create(offer=offer,order=order)
            
        cpls = CartProduct.objects.filter(cart=cart,is_order_generated=False,product_seller__in=[product['product_seller'] for product in products])
        offerss = [product['offers'] for product  in products]
        cpls_offers = zip(cpls,offerss)
        print(cpls_offers,cpls,offerss)
        for cp_ofr in cpls_offers:
            scls = [product['shipping_cost'] for product in products if product['product_seller']==cp_ofr[0].product_seller and 'shipping_cost' in product] 
            
            offers = Offer.objects.filter(id__in=cp_ofr[1])
            gwcls = [product['gift_wrap_charges'] for product in products if product['product_seller']==cp_ofr[0].product_seller and 'gift_wrap_charges' in product]               
            li = Lineitem.objects.create(
                    order = order,
                    product_seller = cp_ofr[0].product_seller,
                    status = 'order-genrated',
                    quantity = cp_ofr[0].quantity,
                    base_price = cp_ofr[0].product_seller.product.base_price,
                    selling_price = cp_ofr[0].product_seller.selling_price,
                    shiping_cost = scls[0] if scls else 0 ,
                    gift_wrap_charges = gwcls[0] if gwcls else 0,
                )
        
            for offer in offers:
                OfferLineitem.objects.create(offer=offer,lineitem=li)
            OrderLog.objects.create(lineitem=li, status='order-genrated',description='order-genrated')
        CartProduct.objects.filter(cart=cart,is_order_generated=False,product_seller__in=[product['product_seller'] for product in products]).update(is_order_generated=True)
        cart.is_cart_processed=True
        cart.save()
        return order

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

class OrderShippingSerializer(serializers.ModelSerializer):
    pass
