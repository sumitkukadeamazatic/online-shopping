"""
    User App Views
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from .models import User, ResetPassword
from .permissions import UserAccessPermission
from .serializers import UserLoginSerializer, UserSerializer, UserResetPasswordSerializer
import sendgrid
import random
from sendgrid.helpers.mail import *
from django.conf import settings


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

    @action(detail=False, methods=['post'])
    def request_reset_password(self, request):
        serializer = UserResetPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            while True:
                otp = random.randint(111111, 999999)
                otp_exists = ResetPassword.objects.filter(otp=otp).first()
                if otp_exists is None:
                    break
            sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)
            from_email = Email(settings.DEFAULT_FROM_MAIL)
            to_email = Email(serializer.data['email'])
            subject = "Amazatic E-commerce Site Reset password OTP"
            content = Content(
                "text/plain", "Hello, Please use following OTP for resetting your password.\n\t %s" % otp)
            mail = Mail(from_email, subject, to_email, content)
#            response = sg.client.mail.send.post(request_body=mail.get())
            user = User.objects.get(email=serializer.data['email'])
            reset_password = ResetPassword.objects.create(
                user=user, otp=otp)
            print(reset_password.otp)
            response_serializer = UserResetPasswordSerializer(
                data=reset_password)
            if response_serializer.is_valid(raise_exception=True):
                return Response(response_serializer.data, status=HTTP_200_OK)
