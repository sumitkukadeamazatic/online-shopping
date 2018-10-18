"""
admin registration and views
"""
from django.contrib import admin
from . import models


class CategoryAdmin(admin.ModelAdmin):
    """
    Category Model Admin
    """
    list_display = ['id', 'name', 'slug', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('name',)}


class FeatureAdmin(admin.ModelAdmin):
    """
     Feature Model Admin
    """
    list_display = ['id', 'name', 'slug', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    """
    Product Model Admin
    """
    list_display = [
        'id',
        'name',
        'slug',
        'description',
        'base_price',
        'created_at',
        'updated_at',
        'images']
    list_filter = ['created_at', 'updated_at']
    list_editable = ['base_price', 'images']
    #prepopulated_fields = {'slug': ('name',)}


class TaxAdmin(admin.ModelAdmin):
    """
    Tax Model Admin
    """
    list_display = [
        'id',
        'name',
        'slug',
        'percent',
        'is_active',
        'created_at',
        'updated_at']
    list_filter = ['percent', 'is_active', 'created_at', 'updated_at']
    list_editable = ['name', 'percent']
    prepopulated_fields = {'slug': ('name',)}


class BrandAdmin(admin.ModelAdmin):
    """
    Brand Model Admin
    """
    list_display = ['id', 'name', 'slug', 'created_at', 'updated_at']
    list_editable = ['name']
    prepopulated_fields = {'slug': ('name',)}


class ProductFeature(admin.ModelAdmin):
    """
    product_feature Model Admin
    """
    inline_type = 'tabular'


class ProductSellerAdmin(admin.ModelAdmin):
    """
    product_seller Model Admin
    """
    list_display = [
        'id',
        'product',
        'seller',
        'quantity',
        'discount',
        'selling_price',
        'min_delivery_days',
        'max_delivery_days',
        'available_pin_codes',
        'is_default']
    list_filter = [
        'quantity',
        'discount',
        'selling_price',
        'min_delivery_days',
        'max_delivery_days']
    list_editable = [
        'quantity',
        'discount',
        'selling_price',
        'min_delivery_days',
        'max_delivery_days']

    def save_form(self, request, form, change):
        """
        Given a ModelForm return an unsaved instance. ``change`` is True if
        the object is being changed, and False if it's being added.
        """
        # check if product-seller relation is new, to set is_default=True
        product_seller_count = models.ProductSeller.objects.filter(
            product=request.POST['product']).count()
        # First relation to be created
        if product_seller_count == 0:
            form.instance.is_default = True
        # only one relation and that is being changed.
        elif product_seller_count == 1 and change:
            form.instance.is_default = True
        elif 'is_default' in request.POST.keys():
            models.ProductSeller.objects.filter(
                product=request.POST['product'], is_default=False).update(is_default=False)
        return form.save(commit=False)


class ReviewAdmin(admin.ModelAdmin):
    """
    Review Model Admin
    """
    list_display = [
        'id',
        'user',
        'seller',
        'product',
        'rating',
        'title',
        'description']
    list_filter = ['rating', 'created_at', 'updated_at']


class WishlistAdmin(admin.ModelAdmin):
    """
    Wishlist Model Admin
    """
    list_display = ['id', 'user', 'product_seller']


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Feature, FeatureAdmin)
admin.site.register(models.Tax, TaxAdmin)
admin.site.register(models.CategoryTax)
admin.site.register(models.Brand, BrandAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductFeature)
admin.site.register(models.ProductSeller, ProductSellerAdmin)
admin.site.register(models.Review, ReviewAdmin)
admin.site.register(models.Wishlist, WishlistAdmin)
