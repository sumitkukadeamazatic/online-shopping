"""
    User App Views
"""

from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserLoginSerializer, UserSerializer
from .models import User


class LoginView(APIView):
    """
       User Login View
    """
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        """
           Login and generate token
        """
        data = request.data
        user_login_serializer = UserLoginSerializer(data=data)
        if user_login_serializer.is_valid(raise_exception=True):
            return Response(user_login_serializer.data)


class UserView(APIView):
    """
       User Model View
    """
    serializer_class = UserSerializer

    def post(self, request, **kwargs):
        if 'id' in kwargs.keys():
            raise exceptions.NotFound()
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()
            return Response(user_serializer.data)

    def put(self, request, **kwargs):
        if not 'id' in kwargs.keys():
            raise exceptions.NotFound()
        user = User.objects.get(pk=kwargs['id'])
        user_serializer = UserSerializer(user, data=request.data)
        print(user_serializer.is_valid())
        return Response({'in': 'progress'})
