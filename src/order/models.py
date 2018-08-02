"""
        Configuration of Modules
"""
from django.contrib.postgres.fields import JSONField
from utils.models import TimestampsAbstract
from user import models as user_model
from seller import models as seller_model
from product import models as product_model
from django.db import models


class Cart(TimestampsAbstract):
    """
        Configuration of CartModules
    """
    user_id = models.ForeignKey(
        user_model.User,
        on_delete=models.CASCADE,
        related_name=None)
    is_cart_processed = models.BooleanField()

    class Meta:
        db_table = 'cart'
        indexes = [
            models.Index(
                fields=[
                    'created_at',
                    'updated_at'],
                name='cart_index')]


class PaymentMethod(TimestampsAbstract):
    """
        Configuration of PaymentMethodModules
    """
    mode = models.CharField(max_length=20)
    slug = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'payment_method'
        indexes = [
            models.Index(
                fields=[
                    'created_at',
                    'updated_at'],
                name='payment_method_index')]


class Order(TimestampsAbstract):
    """
        Configuration of OrderModules
    """
    payment_method_id = models.ForeignKey(
        PaymentMethod,
        on_delete=models.CASCADE,
        related_name=None)
    cart_id = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name=None)
    address_id = models.ForeignKey(
        seller_model.Address,
        on_delete=models.CASCADE,
        related_name=None)
    payment_info = JSONField()
    shipping_name = models.TextField()
    shipping_address_line = models.TextField()
    shipping_city = models.CharField(max_length=60)
    shipping_state = models.CharField(max_length=60)
    shipping_pincode = models.CharField(max_length=10)
    billing_name = models.TextField()
    billing_address_line = models.TextField()
    billing_city = models.CharField(max_length=60)
    billing_state = models.CharField(max_length=60)
    billing_pincode = models.CharField(max_length=10)
    totoal_shipping_cost = models.DecimalField(max_digits=19, decimal_places=2)
    status = models.CharField(max_length=20)

    class Meta:
        db_table = 'order'
        indexes = [
            models.Index(
                fields=[
                    'created_at',
                    'updated_at',
                    'shipping_pincode',
                    'billing_pincode',
                    'shipping_city',
                    'shipping_state',
                    'billing_city',
                    'billing_state'],
                name='order_index')]


class CartProduct(TimestampsAbstract):
    """
        Configuration of CartProductModules
    """
    cart_id = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name=None)
    product_id = models.ForeignKey(
        product_model.Product,
        on_delete=models.CASCADE,
        related_name=None)
    seller_id = models.ForeignKey(
        seller_model.Seller,
        on_delete=models.CASCADE,
        related_name=None)
    quantity = models.PositiveIntegerField()
    is_order_generated = models.BooleanField()

    class Meta:
        db_table = 'cart_product'
        indexes = [
            models.Index(
                fields=[
                    'created_at',
                    'updated_at'],
                name='cart_product_index')]


class Lineitem(TimestampsAbstract):
    """
        Configuration of LineitemModules
    """
    order_id = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name=None)
    product_id = models.ForeignKey(
        product_model.Product,
        on_delete=models.CASCADE,
        related_name=None)
    seller_id = models.ForeignKey(
        seller_model.Seller,
        on_delete=models.CASCADE,
        related_name=None)
    status = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()
    base_price = models.DecimalField(max_digits=19, decimal_places=2)
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True)
    shiping_cost = models.DecimalField(
        max_digits=19, decimal_places=2, blank=True, null=True)
    selling_price = models.DecimalField(max_digits=19, decimal_places=2)
    gift_wrap_charges = models.DecimalField(
        max_digits=19, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'lineitem'
        indexes = [
            models.Index(
                fields=[
                    'created_at',
                    'updated_at',
                    'status'],
                name='lineitem_index')]


class OrderLog(TimestampsAbstract):
    """
        Configuration of OrderLogModules
    """
    lineitem_id = models.ForeignKey(
        Lineitem,
        on_delete=models.CASCADE,
        related_name=None)
    status = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'order_log'
        indexes = [
            models.Index(
                fields=[
                    'created_at',
                    'updated_at'],
                name='order_log_index')]


class ShippingDetails(TimestampsAbstract):
    """
        Configuration of ShippingDetailsModules
    """
    courior_name = models.CharField(max_length=50)
    tracking_number = models.CharField(max_length=50)
    deliverd_date = models.DateField(blank=True, null=True)
    tracking_url = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'shipping_details'
        indexes = [
            models.Index(
                fields=[
                    'created_at',
                    'updated_at',
                    'tracking_number',
                    'deliverd_date',
                    'courior_name'],
                name='shiping_details_index')]


class LineShippingDetails(TimestampsAbstract):
    """
        Configuration of LineShippingDetailsModules
    """
    lineitem_id = models.ForeignKey(
        Lineitem,
        on_delete=models.CASCADE,
        related_name=None)
    shiping_details_id = models.ForeignKey(
        ShippingDetails,
        on_delete=models.CASCADE,
        related_name=None)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'line_shiping_details'
        indexes = [
            models.Index(
                fields=[
                    'created_at',
                    'updated_at'],
                name='line_shiping_details_index')]


class LineitemTax(TimestampsAbstract):
    """
        Configuration of LineitemTaxModules
    """
    lineitem_id = models.ForeignKey(
        Lineitem,
        on_delete=models.CASCADE,
        related_name=None)
    tax_name = models.CharField(max_length=20)
    discount = models.DecimalField(max_digits=4, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=19, decimal_places=2)

    class Meta:
        db_table = 'lineitem_tax'
        indexes = [
            models.Index(
                fields=[
                    'created_at',
                    'updated_at',
                    'tax_name'],
                name='lineitem_tax_index')]
