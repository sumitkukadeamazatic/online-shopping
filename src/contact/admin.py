"""
   Contact App Admin site configuration and model registration
"""

from django.contrib import admin
from .models import Address

# Register your models here.


class AddressAdmin(admin.ModelAdmin):
    """
        Address Model Admin
    """
    list_display = ['original_name', 'name', 'city', 'state', 'pincode']


admin.site.register(Address, AddressAdmin)
