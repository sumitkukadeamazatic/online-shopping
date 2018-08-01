from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.Offer)
admin.site.register(models.OrderOffer)
admin.site.register(models.ProductOffer)
admin.site.register(models.UserOffer)
admin.site.register(models.OfferLineitem)