from django.contrib import admin
from . import models

# Register your models here.


class SellerAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'contact_number', 'get_user_name']


admin.site.register(models.Seller, SellerAdmin)


class AddressAdmin(admin.ModelAdmin):
    list_display = ['original_name', 'name', 'city', 'state', 'pincode']


admin.site.register(models.Address, AddressAdmin)
