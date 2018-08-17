"""
    User App Views
"""

from rest_framework import exceptions, viewsets
from rest_framework.decorators import action, detail_route
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from .serializers import UserLoginSerializer, UserSerializer
from .models import User


class UserViewSet(viewsets.ModelViewSet):
    """
        User Model Viewset
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        if self.action in ['list','auth']:
            queryset = User.objects.all()
        elif self.kwargs['pk'] == str(self.request.user.id):
            queryset = User.objects.filter(pk=self.kwargs['pk'])
        else:
            queryset = []
        return queryset
    
    def get_permissions(self, *args):
        if self.action in ['auth','create']:
            permission_classes = [AllowAny]
        elif self.action is 'list':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

        
    @action(detail=False, methods=['post'])
    def auth(self, request):
        data = request.data
        user_login_serializer = UserLoginSerializer(data=data)
        if user_login_serializer.is_valid(raise_exception=True):
            return Response(user_login_serializer.data)

