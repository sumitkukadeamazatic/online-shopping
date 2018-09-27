'''Custom permissions'''
from rest_framework.permissions import BasePermission, AllowAny

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
        return False

def _user_access(action):
    '''if user is authorised he has all permissions'''
    allowed = ['list', 'retrieve']
    if action in allowed:
        permission_classes = [AllowAny]
    else:
        permission_classes = [UserAccessPermission]
    return [permission() for permission in permission_classes]
