"""
      This serializers script having cart and order api erlizer classes
"""
import json
from rest_framework import serializers
from order.models import Cart, CartProduct, Order, OrderLog, Lineitem, PaymentMethod, LineShippingDetails, ShippingDetails, LineitemTax
from product.models import ProductSeller, CategoryTax
from contact.models import Address
from offer.models import Offer, OrderOffer, OfferLineitem

class CartProductSerializer(serializers.ModelSerializer):
    """
     This serializer class is used in Cart API
    """
    slug = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    img = serializers.SerializerMethodField()
    in_stock = serializers.SerializerMethodField()

    class Meta:
        model = CartProduct
        fields = ('id', 'cart', 'slug', 'name', 'price', 'in_stock', 'quantity', 'img')
        extra_kwargs = {
            'cart': {
                'required': False
            }
        }

    def get_slug(self, obj):   #pylint: disable=no-self-use
        """
            this method return product slug
        """
        return obj.product_seller.product.slug

    def get_name(self, obj):  #pylint: disable=no-self-use
        """
           this method return product name
        """
        return obj.product_seller.product.name

    def get_price(self, obj): #pylint: disable=no-self-use
        """
           this method return selling price
        """
        return obj.product_seller.selling_price

    def get_img(self, obj): #pylint: disable=no-self-use
        """
           This method is used to get imagess
        """
        return obj.product_seller.product.images

    def get_in_stock(self, obj): #pylint: disable=no-self-use
        """
           this method is return is product exist
        """
        return obj.product_seller.quantity > 0

    def validate_quantity(self, value): #pylint: disable=no-self-use
        """
          This method is used to validate quantity
        """
        if value < 0:
            raise serializers.ValidationError("quantity not less than 0")
        return value

    def validate(self, data): #pylint: disable=arguments-differ
        """
           this method is used to validate product seller request data
        """
        if not ProductSeller.objects.filter(pk=self.context['request'].data['product_seller']):
            raise serializers.ValidationError("%s not valid product_seller id"%(self.context['request'].data['product_seller']))
        return data

    def create(self, obj):  #pylint: disable=arguments-differ
        """
           this method is used to create cart product
        """
        cart = Cart.objects.get_or_create(user=self.context['request'].user, is_cart_processed=False)[0]
        product_seller = ProductSeller.objects.get(pk=self.context['request'].data['product_seller'])
        return CartProduct.objects.create(cart=cart, quantity=obj['quantity'], product_seller=product_seller, is_order_generated=self.context['request'].data['is_order_generated'])


def get_discount_amount(offer_ids, amount):
    """
       This method is used to calulate discount
    """
    offers = Offer.objects.filter(id__in=offer_ids).values_list('amount', 'percentage')
    for offer in offers:
        if offer[0]:
            amount -= offer[0]
        else:
            amount -= (amount*offer[1]/100)
    return amount


class OrderSerializer(serializers.ModelSerializer):
    """
       this serializer class is used in Order API
    """
    order_place_date = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    shipping_address = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'order_place_date', 'total_price', 'shipping_address', 'products')

    def get_order_place_date(self, obj): #pylint: disable=no-self-use
        """
           this method is used to order place date
        """
        return OrderLog.objects.get(lineitem__order=obj).created_at.date()

    def get_total_price(self, obj):   #pylint: disable=no-self-use
        """
            this method is used to get total price of order.
        """
        offers = Offer.objects.filter(id__in=OrderOffer.objects.filter(order=obj).values_list('offer'))
        lis = Lineitem.objects.filter(order=obj)
        tprice = 0
        for lineitem in lis:
            tprice += (get_discount_amount(OfferLineitem.objects.filter(lineitem=lineitem).values_list('offer'), lineitem.selling_price) + lineitem.gift_wrap_charges) * lineitem.quantity
        discount_price = tprice
        discount_price = get_discount_amount(offers, tprice)
        return discount_price + obj.totoal_shipping_cost

    def get_shipping_address(self, obj): #pylint: disable=no-self-use
        """
            this method is used to get shipping address
        """
        return {'name' : obj.shipping_name, 'address_line' : obj.shipping_address_line, 'pincode' : obj.shipping_pincode, 'phone_number' : obj.shipping_contact_no}

    def get_products(self, obj): #pylint: disable=no-self-use
        """
           this method is used to get product info list
        """
        lis = Lineitem.objects.filter(order=obj)
        data = []
        for lineitem in lis:
            data.append({"product_name" : lineitem.product_seller.product.name, "price" : lineitem.selling_price, "img" : lineitem.product_seller.product.images})
        return data

    def validate(self, data): #pylint: disable=arguments-differ
        """
           this method is used to validate extra data whiout in serilizer data
        """
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
            if not  CartProduct.objects.filter(cart=self.context['request'].data['cart'], is_order_generated=False, product_seller=product['product_seller']):
                raise serializers.ValidationError("%s is not a vaid product_seller id"%(product['product_seller']))
        return data


    def create(self, validate_data): #pylint: disable=arguments-differ, too-many-locals, unused-argument
        """
           this method is used to create a oreder
        """
        cart = Cart.objects.get(pk=self.context['request'].data['cart'])
        bill_address = Address.objects.get(pk=self.context['request'].data['bill_address'])
        shipping_address = Address.objects.get(pk=self.context['request'].data['shipping_address'])
        offers = Offer.objects.filter(id__in=json.loads(self.context['request'].data['offers']))
        payment_method = PaymentMethod.objects.get(pk=self.context['request'].data['payment_method'])
        products = json.loads(self.context['request'].data['products'])
        order = Order.objects.create(
            payment_method=payment_method,
            cart=cart,
            shipping_name=shipping_address.name,
            shipping_address_line=shipping_address.address_line,
            shipping_contact_no=shipping_address.contact_no,
            shipping_city=shipping_address.city,
            shipping_state=shipping_address.state,
            shipping_pincode=shipping_address.pincode,
            billing_name=bill_address.name,
            billing_address_line=bill_address.address_line,
            billing_city=bill_address.city,
            billing_state=bill_address.state,
            billing_pincode=bill_address.pincode,
            totoal_shipping_cost=sum([product['shipping_cost'] for product in products if 'shipping_cost' in product]),
            status='order-genrated'
        )

        for offer in offers:
            OrderOffer.objects.create(offer=offer, order=order)

        cpls = CartProduct.objects.filter(cart=cart, is_order_generated=False, product_seller__in=[product['product_seller'] for product in products])
        offerss = [product['offers'] for product  in products]
        cpls_offers = zip(cpls, offerss)
        print(cpls, offerss)
        for cp_ofr in cpls_offers:
            scls = [product['shipping_cost'] for product in products if product['product_seller'] == cp_ofr[0].product_seller and 'shipping_cost' in product]
            offers = Offer.objects.filter(id__in=cp_ofr[1])
            gwcls = [product['gift_wrap_charges'] for product in products if product['product_seller'] == cp_ofr[0].product_seller and 'gift_wrap_charges' in product]
            lineitem = Lineitem.objects.create(order=order, product_seller=cp_ofr[0].product_seller, status='order-genrated', quantity=cp_ofr[0].quantity, base_price=cp_ofr[0].product_seller.product.base_price, selling_price=cp_ofr[0].product_seller.selling_price, shiping_cost=scls[0] if scls else 0, gift_wrap_charges=gwcls[0] if gwcls else 0)
            category_tax = CategoryTax.objects.get(category=cp_ofr[0].product_seller.product.category)
            LineitemTax.objects.create(lineitem=lineitem, tax_name=category_tax.tax.name, percentage=category_tax.percentage, tax_amount=lineitem.selling_price*category_tax.percentage/100)
            for offer in offers:
                OfferLineitem.objects.create(offer=offer, lineitem=lineitem)
            OrderLog.objects.create(lineitem=lineitem, status='order-genrated', description='order-genrated')
        cpls.update(is_order_generated=True)
        cart.is_cart_processed = True
        cart.save()
        return order


class TaxSerializer(serializers.ModelSerializer):
    """
        this serializer class is uded to tax serializer
    """
    name = serializers.SerializerMethodField()
    class Meta:
        model = CategoryTax
        fields = ('name', 'percentage')
    def get_name(self, obj):  #pylint: disable=no-self-use
        """
            this method is used to get tax name
        """
        return obj.tax.name


class TaxInvoiceSerializer(serializers.ModelSerializer):
    """
        this serializer is used to tax invoice serializer
    """
    product_name = serializers.SerializerMethodField()
    tax_type = serializers.SerializerMethodField()
    tax_rate = serializers.SerializerMethodField()

    class Meta:
        model = Lineitem
        fields = ('product_name', 'quantity', 'selling_price', 'tax_type', 'tax_rate')

    def get_product_name(self, obj): #pylint: disable=no-self-use
        """
            this mthod id used to get product name
        """
        print(obj)
        return obj.product_seller.product.name
    def get_tax_type(self, obj): #pylint: disable=no-self-use
        """
            this method is used to get tax type
        """
        return LineitemTax.objects.filter(lineitem=obj).tax_name
    def get_tax_rate(self, obj): #pylint: disable=no-self-use
        """
            this method is used to get tax rate
        """
        return LineitemTax.objects.filter(lineitem=obj).tax_amount


class OrderShippingSerializer(serializers.ModelSerializer):
    """
        this serializer class is used in order shiping serializer
    """
    class Meta:
        model = ShippingDetails
        fields = '__all__'

    def create(self, valid_data): #pylint: disable=no-self-use, arguments-differ
        """
            This method is used to create Order shipping serializer
        """
        shipping_details = ShippingDetails.objects.create(courior_name=valid_data['courior_name'], tracking_number=valid_data['tracking_number'], deliverd_date=valid_data['deliverd_date'], tracking_url=valid_data['tracking_url'])
        lqls = json.loads(self.context['request'].data['lineitem_quantity'])
        for lineitem_quantity in lqls:
            LineShippingDetails.objects.create(lineitem=Lineitem.objects.get(id=lineitem_quantity['lineitem']), quantity=lineitem_quantity['quantity'], shipping_details=shipping_details, description=lineitem_quantity['description'])
        return shipping_details
