"""
     Seller App Admin Settings
"""
from django.contrib import admin
from . import models

# Register your models here.


class SellerAdmin(admin.ModelAdmin):
    """
        Seller Model admin
    """
    list_display = ['company_name', 'contact_number']


admin.site.register(models.Seller, SellerAdmin)

class SellerUserAdmin(admin.ModelAdmin):
    """
        SellerUser Model admin
    """
    list_display = ['seller_id', 'user_id']

admin.site.register(models.SellerUser, SellerUserAdmin)
