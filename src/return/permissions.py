"""
Return App Custom permissions classes
"""

from rest_framework import permissions


class ReturnAccessPermission(permissions.BasePermission):
    """
    Custom class to restrict return related actions
    """
    message = 'Access Denied.'

    def has_permission(self, request, view):
        if request.auth:
            if view.action in ['create', 'list', 'create_lineitem_shipping_detail']:
                return True
        return False
