from rest_framework.permissions import BasePermission


class UserAccessPermission(BasePermission):
    """
         UserViewSet Permissions
    """

    message = "Access Denied."
    
    def has_permission(self, request, view):
        print(view.action)
        if not request.auth:
            return False
        allowed_actions = ['create', 'list','payment', 'retrieve', 'shipping']
        if view.action in allowed_actions:
            return True
        return  False
