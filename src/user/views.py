"""
    User App Views
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User
from .permissions import UserAccessPermission
from .serializers import UserLoginSerializer, UserSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse


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


def request_forgot_password(request):
    send_mail('Testing', "First Email through DRF", settings.EMAIL_HOST_USER, [
              request.POST['email']], fail_silently=False)
    return JsonResponse({'message': 'Working'})
