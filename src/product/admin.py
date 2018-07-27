from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.Category)
admin.site.register(models.Feature)
admin.site.register(models.Tax)
admin.site.register(models.CategoryTax)
admin.site.register(models.Brand)
admin.site.register(models.Product)
admin.site.register(models.ProductFeature)
admin.site.register(models.ProductSeller)
admin.site.register(models.Review)
admin.site.register(models.Wishlist)
