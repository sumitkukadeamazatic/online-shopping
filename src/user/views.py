"""
    User App Views
"""
import random
from datetime import datetime, timedelta
from django.contrib.auth import login
from django.conf import settings
from rest_framework.exceptions import ParseError
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail
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
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(email=serializer.data['email'])
            now = datetime.now()
            possible_otp_time = now - timedelta(minutes=5)
            reset_password = ResetPassword.objects.filter(
                user_id=user.id, is_validated=False, is_reset=False, created_at__gte=possible_otp_time).first()
            if reset_password:
                otp = reset_password.otp
            else:
                while True:
                    otp = random.randint(111111, 999999)
                    otp_exists = ResetPassword.objects.filter(
                        otp=otp, is_validated=True).first()
                    if otp_exists is None:
                        break
                ResetPassword.objects.create(
                    user=user, otp=otp)
            if settings.APP_ENVIRONMENT == 'production':
                sendgrid_inst = sendgrid.SendGridAPIClient(
                    apikey=settings.SENDGRID_API_KEY)
                from_email = Email(settings.DEFAULT_FROM_MAIL)
                to_email = Email(serializer.data['email'])
                subject = "Amazatic Dummy E-commerce Site Reset password"
                content = Content(
                    "text/plain", "Hello, Please use following OTP for resetting your password.\n\t %s" % otp)
                mail = Mail(from_email, subject, to_email, content)
                mail_response = sendgrid_inst.client.mail.send.post(
                    request_body=mail.get())
                if not mail_response.status_code in [200, 202]:
                    raise ParseError(detail='Not able to send email.')
            response_serializer = RequestResetPasswordSerializer(
                data={'message': 'OTP has been sent to your registered Email address', 'email': serializer.data['email']})
            if response_serializer.is_valid(raise_exception=True):
                return Response(response_serializer.data, status=HTTP_200_OK)
        return False

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
