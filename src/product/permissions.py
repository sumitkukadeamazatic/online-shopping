from rest_framework.permissions import BasePermission


class UserAccessPermission(BasePermission):
    """
         UserViewSet Permissions
    """

    message = "Access Denied."
    
    def has_permission(self, request, view):
        if not request.auth:
            return False
        if view.action == 'create' or view.action == 'list' or view.action == 'destroy' or view.action == 'partial_update' or view.action == 'retrieve':
            return True
        return  False