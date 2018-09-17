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
        if view.action in ['create', 'request_reset_password', 'validate_reset_password', 'reset_password'] and request.method == 'POST':
            is_allowed = True
        elif view.action == 'list':
            if request.user.is_superuser:  # pylint: disable=simplifiable-if-statement
                is_allowed = True
            else:
                is_allowed = False
        # actions retrieve, update, partial_update need user to authenticated and restricting destroy action for all users
        elif request.auth and view.action != 'destroy':
            # Allowing superuser and the authenticated user to retrieve, update the data of that particular user only.
            if (str(request.user.id) == view.kwargs['pk']) or request.user.is_superuser:  # pylint: disable=simplifiable-if-statement
                is_allowed = True
            else:
                is_allowed = False
        else:
            is_allowed = False
        return is_allowed
