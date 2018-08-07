"""
    User App Views
"""

from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
# from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import LoginSerializer


@csrf_exempt
def login(request):
    """
           Login and generate token
    """
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(email=email, password=password)
    if user is None:
        pass
    token = Token.objects.get_or_create(user=user)
    data = {
        'message': 'Login successful',
        'token': token[0]
    }
    loginResponse = LoginSerializer(data)
    return JsonResponse(loginResponse.data)


def auth_test(request):
    print(request.REQUEST)
    pass
