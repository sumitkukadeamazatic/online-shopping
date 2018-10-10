"""
        Configuration of Modules
"""
from user import models as user_model
from django.contrib.postgres.fields import JSONField
from django.db import models
from utils.models import CustomBaseModelMixin
from product import models as product_model


class Cart(CustomBaseModelMixin):
    """
        Configuration of CartModules
    """
    user = models.ForeignKey(
        user_model.User,
        on_delete=models.CASCADE,
        related_name=None,blank=True, null=True)
    is_cart_processed = models.BooleanField()


class PaymentMethod(CustomBaseModelMixin):
    """Address
        Configuration oAddressf PAddressymentMethodModules
    """
    mode = models.CharField(max_length=20)
    slug = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.mode


class Order(CustomBaseModelMixin):
    """
        Configuration of OrderModules
    """
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.CASCADE,
        related_name=None)
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name=None)
    payment_info = JSONField(null=True, blank=True)
    shipping_name = models.TextField()
    shipping_address_line = models.TextField()
    shipping_contact_no = models.CharField(
        max_length=20, null=True, blank=True)
    shipping_city = models.CharField(max_length=60)
    shipping_state = models.CharField(max_length=60)
    shipping_pincode = models.CharField(max_length=10)
    billing_name = models.TextField()
    billing_address_line = models.TextField()
    billing_contact_no = models.CharField(max_length=20, null=True, blank=True)
    billing_city = models.CharField(max_length=60)
    billing_state = models.CharField(max_length=60)
    billing_pincode = models.CharField(max_length=10)
    totoal_shipping_cost = models.DecimalField(max_digits=19, decimal_places=2)
    status = models.CharField(max_length=20)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'shipping_pincode',
                    'billing_pincode',
                    'shipping_city',
                    'shipping_state',
                    'billing_city',
                    'billing_state'],
                name='order_index')]

    def __str__(self):
        return "Order No. %s" % self.id  # pylint: disable=no-member


class CartProduct(CustomBaseModelMixin):
    """
        Configuration of CartProductModules
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name=None)
    product_seller = models.ForeignKey(
        product_model.ProductSeller,
        on_delete=models.CASCADE,
        related_name=None)
    quantity = models.PositiveIntegerField()
    is_order_generated = models.BooleanField()


class Lineitem(CustomBaseModelMixin):
    """
        Configuration of LineitemModules
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name=None)
    product_seller = models.ForeignKey(
        product_model.ProductSeller,
        on_delete=models.CASCADE,
        related_name=None)
    status = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()
    base_price = models.DecimalField(max_digits=19, decimal_places=2)
    shiping_cost = models.DecimalField(
        max_digits=19, decimal_places=2, blank=True, null=True)
    selling_price = models.DecimalField(max_digits=19, decimal_places=2)
    gift_wrap_charges = models.DecimalField(
        max_digits=19, decimal_places=2, blank=True, null=True)

    def __str__(self):
        product_name = product_model.ProductSeller.objects.filter(
            pk=self.product_seller_id).values('product__name').first()
        return "Order No. %s - %s" % (self.order_id, product_name['product__name'])


class OrderLog(CustomBaseModelMixin):
    """
        Configuration of OrderLogModules
    """
    lineitem = models.ForeignKey(
        Lineitem,
        on_delete=models.CASCADE,
        related_name=None)
    status = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)


class ShippingDetails(CustomBaseModelMixin):
    """
        Configuration of ShippingDetailsModules
    """
    courior_name = models.CharField(max_length=50)
    tracking_number = models.CharField(max_length=50)
    deliverd_date = models.DateField(blank=True, null=True)
    tracking_url = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'tracking_number',
                    'deliverd_date',
                    'courior_name'],
                name='shiping_details_index')]

    def __str__(self):
        return '%s - %s' % (self.courior_name, self.tracking_number)


class LineShippingDetails(CustomBaseModelMixin):
    """
        Configuration of LineShippingDetailsModules
    """
    lineitem = models.ForeignKey(
        Lineitem,
        on_delete=models.CASCADE,
        related_name=None)
    shipping_details = models.ForeignKey(
        ShippingDetails,
        on_delete=models.CASCADE,
        related_name=None)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)


class LineitemTax(CustomBaseModelMixin):
    """
        Configuration of LineitemTaxModules
    """
    lineitem = models.ForeignKey(
        Lineitem,
        on_delete=models.CASCADE,
        related_name=None)
    tax_name = models.CharField(max_length=20)
    percentage = models.DecimalField(max_digits=4, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=19, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'tax_name'],
                name='lineitem_tax_index')]
