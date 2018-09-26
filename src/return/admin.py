"""Admin
    All Return related Admin
"""
from django.shortcuts import render
from django.contrib import admin
from django_admin_row_actions import AdminRowActionsMixin
from . import models

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    """ Admin Model
        return_order_admin model
    """
    list_display = ['order_id', 'status', 'created_at', 'updated_at']
    list_filter = ['order_id', 'status', 'created_at', 'updated_at']


admin.site.register(models.Order, OrderAdmin)


class LineitemAdmin(AdminRowActionsMixin, admin.ModelAdmin):
    """ Admin Model
        return_lineitem_admin model
    """
    list_display = ['return_order_id', 'lineitem_id', 'quantity',
                    'reason', 'description', 'status', 'created_at', 'updated_at']
    list_filter = ['return_order_id', 'status',
                   'reason', 'created_at', 'updated_at']
    # list_editable = ['status', 'reason']

    def change_status(self, request, obj):
        if request.method == 'GET':
            status_choices = dict(models.Lineitem.STATUS_CHOICES_FIELDS)
            object_status = (obj.status, status_choices[obj.status])
            print(object_status[0])
            context = {
                'status_choices': dict(models.Lineitem.STATUS_CHOICES_FIELDS),
                'current_status_name': status_choices[obj.status],
                'object_status': obj.status
            }

            print(context)
            return render(request, 'change_status.html', context=context)
        print('method is post')
        print((request.POST), '*********************')
        print(obj.__class__)

    def get_row_actions(self, obj):
        row_actions = [
            {
                'label': 'Change status',
                'action': 'change_status',
            },
        ]
        row_actions += super(LineitemAdmin, self).get_row_actions(obj)
        return row_actions


admin.site.register(models.Lineitem, LineitemAdmin)


class OrderLogAdmin(admin.ModelAdmin):
    """ Admin Model
        return_order_log_admin model
    """
    list_display = ['return_lineitem_id', 'status',
                    'description', 'created_at', 'updated_at']
    list_filter = ['return_lineitem_id', 'status', 'created_at', 'updated_at']
    list_editable = ['status']


admin.site.register(models.OrderLog, OrderLogAdmin)


class LineitemShippingDetailAdmin(admin.ModelAdmin):
    """ Admin Model
        return_lineitem_shipping_detail_admin model
    """
    list_display = ['shipping_detail_id', 'return_lineitem_id',
                    'quantity', 'description', 'created_at', 'updated_at']
    list_filter = ['shipping_detail_id', 'return_lineitem_id',
                   'quantity', 'created_at', 'updated_at']
    list_editable = ['quantity']


admin.site.register(models.LineitemShippingDetail,
                    LineitemShippingDetailAdmin)
