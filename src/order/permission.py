"""
    User App Permission
"""
from rest_framework.permissions import BasePermission


class CartPermissions(BasePermission):
    """
         UserViewSet Permissions
    """

    message = "Add cart in request"

    def has_permission(self, request, view):
        if not request.auth and 'cart' not in request.data:
            return False
        return True
        
