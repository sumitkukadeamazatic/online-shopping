"""
    User App Views
"""
from datetime import datetime, timedelta
from django.contrib.auth import login
from rest_framework.exceptions import ParseError
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from knox.views import LoginView as KnoxLoginView
from .models import User, ResetPassword
from .permissions import UserAccessPermission
from .serializers import UserLoginSerializer, UserSerializer, RequestResetPasswordSerializer, ValidateResetPasswordSerializer, ResetPasswordSerializer, ResponseResetPasswordSerializer


class UserViewSet(ModelViewSet):        # pylint: disable=too-many-ancestors
    """
    User Model Viewset
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [UserAccessPermission]

    @action(detail=False, methods=['post'], url_path='reset-password')
    def request_reset_password(self, request):  # pylint: disable=no-self-use
        """
        Request Reset Password API
        """
        serializer = RequestResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='reset-password/validate')
    def validate_reset_password(self, request):    # pylint: disable=no-self-use
        """
            Validate Reset Password request using OTP
        """
        validate_serializer = ValidateResetPasswordSerializer(
            data=request.POST)
        if validate_serializer.is_valid(raise_exception=True):
            response_serializer = ResponseResetPasswordSerializer(
                data={'message': 'Data validated successfully.'})
            if response_serializer.is_valid(raise_exception=True):
                return Response(response_serializer.data, status=HTTP_200_OK)
        return False

    @action(detail=False, methods=['post'], url_path='reset-password/reset')
    def reset_password(self, request):      # pylint: disable=no-self-use
        """
            Reset Password
        """
        reset_serializer = ResetPasswordSerializer(data=request.POST)
        if reset_serializer.is_valid(raise_exception=True):
            user = User.objects.get(email=reset_serializer.data['email'])
            user.set_password(reset_serializer.data['password'])
            user.save()
            ResetPassword.objects.filter(
                id=reset_serializer.data['reset_password_id']).update(is_reset=True)
            response_serializer = ResponseResetPasswordSerializer(
                data={'message': 'Password Reset successfull.'})
            if response_serializer.is_valid(raise_exception=True):
                return Response(response_serializer.data, status=HTTP_200_OK)
        return False


class UserLoginView(KnoxLoginView):
    """
       Login View overriding the base knox login view
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):  # pylint: disable=redefined-builtin
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        return super(UserLoginView, self).post(request, format=None)
