"""
    User App Permission
"""
from rest_framework.permissions import BasePermission


class UserAccessPermission(BasePermission):
    """
         UserViewSet Permissions
    """

    message = "Access Denied."

    def has_permission(self, request, view):
        if view.action in ['auth', 'create']:
            return True
        elif view.action == 'list':
            if request.user.is_superuser:
                return True
            else:
                return False
        elif request.auth and view.action != 'destroy':
            if str(request.user.id) == view.kwargs['pk'] or request.user.is_superuser:
                return True
            else:
                return False
        else:
            return False
