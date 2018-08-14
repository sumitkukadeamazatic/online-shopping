"""
    User App Views
"""

# from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
# from rest_framework.decorators import api_view
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LoginSerializer
from rest_framework import generics, exceptions
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict


class LoginView(APIView):

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """
           Login and generate token
        """
        email = request.data.get('email')
        password = request.data.get('password')
        data = request.data
        serializerTest = LoginSerializer(data=data)
        if not serializerTest.is_valid():
            raise exceptions.ParseError(detail=serializerTest.errors)
        user = authenticate(email=email, password=password)
        if user is None:
            raise exceptions.AuthenticationFailed(detail='Invalid Credentials')
        userDict = model_to_dict(user)
        serializer = LoginSerializer(data=userDict)
        if not serializer.is_valid():
            raise exceptions.ParseError(detail=serializer.errors)
        return Response(serializer.data)
#        email = request.POST.get('email')
#        password = request.POST.get('password')
#        user = authenticate(email=email, password=password)
#        if user is None:
#            raise exceptions.AuthenticationFailed(detail='Invalid Credentials')
#        token = Token.objects.get_or_create(user=user)
#        print(token)
#        data = {
#            'message': 'Login successful',
#            'token': token[0]
#        }
#        loginResponse = LoginSerializer(data)
#        return Response(loginResponse.data)


class AuthenticateTest(generics.GenericAPIView):
    # @login_required
    def post(self, request):
        print(request.__class__)
        print(request.data)
        print(request.POST.get('test1'))
        return JsonResponse({'message': 'Working'})


class SecondTestView(generics.GenericAPIView):

    def post(self, request):
        print('in second')
        print(request.data)
        return Response({'key': 'working'})


class ThirdTestView(generics.GenericAPIView):

    def post(self, request):
        return Response({'message': 'Third working'})
