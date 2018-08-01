from django.contrib import admin
from . import models

# Register your models here.


class ReturnOrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'status', 'created_at', 'updated_at']
    list_filter = ['order_id', 'status', 'created_at', 'updated_at']
    list_editable = ['status']


admin.site.register(models.ReturnOrder, ReturnOrderAdmin)


class ReturnLineitemAdmin(admin.ModelAdmin):
    list_display = ['return_order_id', 'lineitem_id', 'quantity',
                    'reason', 'description', 'status', 'created_at', 'updated_at']
    list_filter = ['return_order_id', 'status',
                   'reason', 'created_at', 'updated_at']
    list_editable = ['status', 'reason']


admin.site.register(models.ReturnLineitem, ReturnLineitemAdmin)


class ReturnOrderLogAdmin(admin.ModelAdmin):
    list_display = ['return_lineitem_id', 'status',
                    'description', 'created_at', 'updated_at']
    list_filter = ['return_lineitem_id', 'status', 'created_at', 'updated_at']
    list_editable = ['status']


admin.site.register(models.ReturnOrderLog, ReturnOrderLogAdmin)


class ReturnLineitemShippingDetailAdmin(admin.ModelAdmin):
    list_display = ['shipping_detail_id', 'return_lineitem_id',
                    'quantity', 'description', 'created_at', 'updated_at']
    list_filter = ['shipping_detail_id', 'return_lineitem_id',
                   'quantity', 'created_at', 'updated_at']
    list_editable = ['quantity']


admin.site.register(models.ReturnLineitemShippingDetail,
                    ReturnLineitemShippingDetailAdmin)
