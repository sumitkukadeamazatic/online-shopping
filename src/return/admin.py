"""Admin
    All Return related Admin
"""
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import admin, messages
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
    list_display = ('return_order_id', 'lineitem_id', 'quantity',
                    'reason', 'description', 'status', 'created_at', 'updated_at')
    list_filter = ('return_order_id', 'status',
                   'reason', 'created_at', 'updated_at')

    def change_status(self, request, obj):  # pylint: disable=inconsistent-return-statements
        """
        function handles both GET and POST method of return change status flow
        """
        if request.method == 'GET':
            status_choices = dict(models.Lineitem.STATUS_CHOICES_FIELDS)
            context = {
                'status_choices': dict(models.Lineitem.STATUS_CHOICES_FIELDS),
                'current_status_name': status_choices[obj.status],
                'object_status': obj.status
            }
            return render(request, 'change_status.html', context=context)
        if request.method == 'POST':  # pylint: disable=no-else-return
            if 'status' in request.POST.keys():  # pylint: disable=no-else-return
                obj.status = request.POST['status']
                obj.save()
                models.OrderLog.objects.create(
                    return_lineitem=obj, status=obj.status, description=request.POST['description'])
                self.message_user(request, "Return order status changed.",
                                  level=messages.INFO)
                return HttpResponseRedirect('/admin/return/lineitem/')
            else:
                self.message_user(request, "Select new status.",
                                  level=messages.ERROR)
        else:
            self.message_user(request, 'Method not allowed.',
                              level=messages.ERROR)

    def get_row_actions(self, obj):
        if obj.status == 'CM':
            row_actions = []
        else:
            row_actions = [
                {
                    'label': 'Change status',
                    'action': 'change_status',
                    'enabled': obj.status != 'CM',
                }
            ]
            row_actions += super(LineitemAdmin, self).get_row_actions(obj)
        return row_actions


admin.site.register(models.Lineitem, LineitemAdmin)


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
