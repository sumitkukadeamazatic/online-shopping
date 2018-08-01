from django.contrib import admin
from . import models
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ['id','user_id','is_cart_processed']
    list_filter = ['is_cart_processed']
    
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['id','mode','slug']
    list_filter = ['mode','created_at', 'updated_at']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','payment_method_id','cart_id','address_id','payment_info','shipping_name','shipping_address_line','billing_name','billing_address_line','totoal_shipping_cost','status','created_at', 'updated_at','shipping_pincode','billing_pincode','shipping_city','shipping_state','billing_city','billing_state']
    list_filter = ['created_at', 'updated_at','shipping_pincode','billing_pincode','shipping_city','shipping_state','billing_city','billing_state']

class CartProductAdmin(admin.ModelAdmin):
    list_display = ['id','cart_id','product_id','seller_id','quantity','is_order_generated','created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at','is_order_generated','quantity']

class LineitemAdmin(admin.ModelAdmin):
    list_display = ['id','order_id','product_id','seller_id','status','quantity','base_price','discount','shiping_cost','selling_price','gift_wrap_charges','created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at', 'status']

class OrderLogAdmin(admin.ModelAdmin):
    list_display = ['id','lineitem_id','status','description']
    list_filter = ['created_at', 'updated_at']

class ShippingDetailsAdmin(admin.ModelAdmin):
    list_display = ['id','courior_name','tracking_number','deliverd_date','tracking_url','created_at', 'updated_at']
    list_filter =  ['created_at', 'updated_at','tracking_number','deliverd_date','courior_name']

class LineShippingDetailsAdmin(admin.ModelAdmin):
    list_display = ['id','lineitem_id','shiping_details_id','quantity','description']
    list_filter = ['created_at', 'updated_at']

class LineitemTaxAdmin(admin.ModelAdmin):
    list_display = ['id','lineitem_id','tax_name','discount','tax_amount']
    list_filter = ['created_at', 'updated_at','tax_name']

admin.site.register(models.Order)
admin.site.register(models.Cart)
admin.site.register(models.CartProduct)
admin.site.register(models.Lineitem)
admin.site.register(models.LineitemTax)
admin.site.register(models.LineShippingDetails)
admin.site.register(models.OrderLog)
admin.site.register(models.PaymentMethod)
admin.site.register(models.ShippingDetails)