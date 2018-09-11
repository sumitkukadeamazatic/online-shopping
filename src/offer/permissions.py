"""
    Offer App Permission
"""
from rest_framework.permissions import BasePermission


class OfferPermission(BasePermission):
    """
         OfferViewSet Permissions
    """

    message = "Access Denied."

    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        return False
