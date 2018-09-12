"""
        Configuration of admin
"""
from django.contrib import admin
from . import models
# Register your models here.


class OfferAdmin(admin.ModelAdmin):
    """
        Configuration of OfferAdmin
    """
    list_display = ['id', 'name', 'slug', 'description', 'code', 'amount', 'percentage', 'is_for_order', 'minimum',
                    'amount_limit', 'for_new_user', 'valid_from', 'valid_upto', 'start_time', 'end_time', 'days', 'max_count']
    list_filter = ['created_at', 'updated_at', 'valid_from', 'valid_upto',
                   'name', 'is_for_order', 'amount', 'percentage', 'for_new_user']
    list_editable = ['valid_from', 'valid_upto', 'name', 'is_for_order',
                     'amount', 'percentage', 'for_new_user', 'description']
    prepopulated_fields = {'slug': ('name',)}


class OrderOfferAdmin(admin.ModelAdmin):
    """
        Configuration of OrderOfferAdmin
    """
    list_display = ['id', 'order', 'offer', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']


class ProductOfferAdmin(admin.ModelAdmin):
    """
        Configuration of ProductOfferAdmin
    """
    list_display = ['id', 'product_id',
                    'offers_id', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']


class UserOfferAdmin(admin.ModelAdmin):
    """
        Configuration of UserOfferAdmin
    """
    list_display = ['id', 'user', 'offer', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']


class OfferLineitemAdmin(admin.ModelAdmin):
    """
        Configuration of OfferLineitemAdmin
    """
    list_display = ['id', 'lineitem',
                    'offer', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']


admin.site.register(models.Offer, OfferAdmin)
admin.site.register(models.OrderOffer, OrderOfferAdmin)
admin.site.register(models.ProductOffer, ProductOfferAdmin)
admin.site.register(models.UserOffer, UserOfferAdmin)
admin.site.register(models.OfferLineitem, OfferLineitemAdmin)
