"""
   User App Admin Settings
"""
from django.contrib import admin
from . import models

# Register your models here.


class RoleAdmin(admin.ModelAdmin):
    """
       Role Model Admin
    """
    fields = ['name', 'slug']
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(models.Role, RoleAdmin)


class UserAdmin(admin.ModelAdmin):
    """
       User Model Admin
    """
    list_display = [
        'email',
        'first_name',
        'last_name',
        'contact_no',
        'gender',
        'dob']


admin.site.register(models.User, UserAdmin)
