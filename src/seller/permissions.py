"""
    Seller App Custom peermission classes
"""

from rest_framework import permissions
from seller.models import *

class SellerAccessPermission(permissions.BasePermission):
    """
        Custom class to restrict seller related actions
    """

    message = "Access Denied."

    def has_permission(self, request, view):
        if request.auth:
            if request.user.is_superuser or view.action == 'list':
                return True
            if int(view.kwargs['pk']) in SellerUser.objects.filter(user=request.user.id).values_list('seller_id', flat=True):
                return True
        return False

class ChangeStatusPermission(permissions.BasePermission):
    """
        Custom class to restrict Change Status related action
    """

    message = "Access Denied."

    def has_permission(self, request, view):
        if request.auth:
            try:
                seller_obj = Seller.objects.get(id=view.kwargs['pk'])
                if seller_obj.is_verified == True and seller_obj.status != 'InProgress':
                    if request.user.is_superuser or int(view.kwargs['pk']) in SellerUser.objects.filter(user=request.user.id).values_list('seller_id', flat=True):
                        return True
            except:
                pass
        return False
