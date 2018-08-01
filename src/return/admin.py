from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.ReturnOrder)
admin.site.register(models.ReturnLineitem)
admin.site.register(models.ReturnOrderLog)
admin.site.register(models.ReturnLineitemShippingDetail)
