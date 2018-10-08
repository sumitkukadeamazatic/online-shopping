"""
    Seller App Custom peermission classes
"""

from rest_framework import permissions

class SellerAccessPermission(permissions.BasePermission):
    """
        Custom class to restrict seller related actions
    """

    message = "Access Denied."

    def has_permission(self, request, view):
        if request.auth:
            return True
        return False
