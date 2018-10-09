"""
        Configuration of admin
"""
from django.contrib import admin
from django.db.models import Q
from django_admin_row_actions import AdminRowActionsMixin
from importlib import import_module
from . import models


class CartAdmin(admin.ModelAdmin):
    """
        Configuration of CartAdmin
    """
    list_display = ['id', 'user_id', 'is_cart_processed']
    list_filter = ['is_cart_processed']


class PaymentMethodAdmin(admin.ModelAdmin):
    """
        Configuration of PaymentMethodAdmin
    """
    list_display = ['id', 'mode', 'slug']
    list_filter = ['mode', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('mode',)}


class OrderAdmin(admin.ModelAdmin):
    """
        Configuration of OrderAdmin
    """
    list_display = ['id', 'payment_method_id', 'cart_id', 'payment_info', 'shipping_name', 'shipping_address_line', 'billing_name', 'billing_address_line',
                    'totoal_shipping_cost', 'status', 'created_at', 'updated_at', 'shipping_pincode', 'billing_pincode', 'shipping_city', 'shipping_state', 'billing_city', 'billing_state']
    list_filter = ['created_at', 'updated_at', 'shipping_pincode', 'billing_pincode',
                   'shipping_city', 'shipping_state', 'billing_city', 'billing_state']


class CartProductAdmin(admin.ModelAdmin):
    """
        Configuration of CartProductAdmin
    """
    list_display = ['id', 'cart_id', 'product_seller', 'quantity',
                    'is_order_generated', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at',
                   'is_order_generated', 'quantity']


class LineitemAdmin(AdminRowActionsMixin, admin.ModelAdmin):
    """
        Configuration of LineitemAdmin
    """

    list_display = ['id', 'order_id', 'product_seller', 'status', 'quantity', 'base_price',
                    'shiping_cost', 'selling_price', 'gift_wrap_charges', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at', 'status']

    def get_row_actions(self, obj):
        shipping_details_relation = models.LineShippingDetails.objects.filter(
            lineitem=obj)
        if shipping_details_relation:
            return []
        row_actions = [
            {
                'label': 'Assign Shipping details',
                'url': '/admin/order/lineshippingdetails/add/'

            }
        ]
        row_actions += super(LineitemAdmin, self).get_row_actions(obj)
        return row_actions


class OrderLogAdmin(admin.ModelAdmin):
    """
        Configuration of OrderLogAdmin
    """
    list_display = ['id', 'lineitem_id', 'status', 'description']
    list_filter = ['created_at', 'updated_at']


class ShippingDetailsAdmin(AdminRowActionsMixin, admin.ModelAdmin):
    """
        Configuration of ShippingDetailsAdmin
    """
    list_display = ['id', 'courior_name', 'tracking_number',
                    'deliverd_date', 'tracking_url', 'created_at']
    list_filter = ['created_at', 'updated_at',
                   'tracking_number', 'deliverd_date', 'courior_name']

    def get_row_actions(self, obj):
        order_relation = models.LineShippingDetails.objects.filter(
            shipping_details=obj).first()
        # need this because can not use "from return.models import *" as "return" is a keyword
        return_models = import_module("return.models")
        return_relation = return_models.LineitemShippingDetail.objects.filter(
            shipping_detail=obj).first()
        if order_relation or return_relation:
            row_actions = []
            return row_actions
        row_actions = [
            {
                'label': 'Assign order lineitem',
                'url': '/admin/order/lineshippingdetails/add/'
            },
            {
                'label': 'Assign Return order lineitem',
                'url': '/admin/return/lineitemshippingdetail/add/'
            }
        ]
        row_actions += super(ShippingDetailsAdmin, self).get_row_actions(obj)
        return row_actions


class LineShippingDetailsAdmin(admin.ModelAdmin):
    """
    Configuration of LineShippingDetailsAdmin
    """
    list_display = ['id', 'lineitem_id',
                    'quantity', 'description']
    list_filter = ['created_at', 'updated_at']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'shipping_details':
            return_models = import_module("return.models")
            kwargs['queryset'] = models.ShippingDetails.objects.filter(~Q(id__in=models.LineShippingDetails.objects.values(
                'shipping_details_id')) & ~Q(id__in=return_models.LineitemShippingDetail.objects.values('shipping_detail_id')))
        return super(LineShippingDetailsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class LineitemTaxAdmin(admin.ModelAdmin):
    """
    Configuration of LineitemTaxAdmin
    """
    list_display = ['id', 'lineitem_id', 'tax_name', 'tax_name', 'tax_amount']
    list_filter = ['created_at', 'updated_at', 'tax_name']


admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Cart, CartAdmin)
admin.site.register(models.CartProduct, CartProductAdmin)
admin.site.register(models.Lineitem, LineitemAdmin)
admin.site.register(models.LineitemTax, LineitemTaxAdmin)
admin.site.register(models.LineShippingDetails, LineShippingDetailsAdmin)
admin.site.register(models.OrderLog, OrderLogAdmin)
admin.site.register(models.PaymentMethod, PaymentMethodAdmin)
admin.site.register(models.ShippingDetails, ShippingDetailsAdmin)
