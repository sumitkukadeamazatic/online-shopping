from rest_framework.permissions import BasePermission


class UserAccessPermission(BasePermission):
    """
         UserViewSet Permissions
    """

    message = "Access Denied."
    
    def has_permission(self, request, view):
        
        if not request.auth:
            return False
        if view.action in ('create', 'list', 'retrieve', 'partial_update', 'destroy'):
            return True
        return  False