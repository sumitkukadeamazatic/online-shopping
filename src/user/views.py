"""
    User App Views
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User
from .permissions import UserAccessPermission
from .serializers import UserLoginSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
        User Model Viewset
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [UserAccessPermission]

    @action(detail=False, methods=['post'])
    def auth(self, request):
        """
             Authentication API (login)
        """
        data = request.data
        user_login_serializer = UserLoginSerializer(data=data)
        if user_login_serializer.is_valid(raise_exception=True):
            return Response(user_login_serializer.data)
