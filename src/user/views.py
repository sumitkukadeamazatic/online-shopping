"""
    User App Views
"""

from rest_framework import exceptions, viewsets
from rest_framework.decorators import action, detail_route
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
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
#    pagination_class = PageNumberPagination

    @action(detail=False, methods=['post'])
    def auth(self, request):
        data = request.data
        user_login_serializer = UserLoginSerializer(data=data)
        if user_login_serializer.is_valid(raise_exception=True):
            return Response(user_login_serializer.data)
