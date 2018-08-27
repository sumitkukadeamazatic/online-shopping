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
        if view.action in ['auth', 'create', 'request_reset_password', 'reset_password_validate', 'reset_password'] and request.method == 'POST':
            is_allowed = True
        elif view.action == 'list':
            if bool(request.user.is_superuser):
                is_allowed = True
            else:
                is_allowed = False
        elif request.auth and view.action != 'destroy':
            if str(request.user.id) == view.kwargs['pk'] or bool(request.user.is_superuser):
                is_allowed = True
            else:
                is_allowed = False
        else:
            is_allowed = False
        return is_allowed
