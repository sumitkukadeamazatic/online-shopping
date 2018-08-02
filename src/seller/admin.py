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
    list_display = ['company_name', 'contact_number', 'get_user_name']


admin.site.register(models.Seller, SellerAdmin)


class AddressAdmin(admin.ModelAdmin):
    """
        Address Model Admin
    """
    list_display = ['original_name', 'name', 'city', 'state', 'pincode']


admin.site.register(models.Address, AddressAdmin)
