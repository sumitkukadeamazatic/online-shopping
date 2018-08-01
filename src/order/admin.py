from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.Order)
admin.site.register(models.Cart)
admin.site.register(models.CartProduct)
admin.site.register(models.Lineitem)
admin.site.register(models.LineitemTax)
admin.site.register(models.LineShippingDetails)
admin.site.register(models.OrderLog)
admin.site.register(models.PaymentMethod)
admin.site.register(models.ShippingDetails)