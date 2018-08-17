"""
     Seller App Views
"""
# from django.shortcuts import render
# Create your views here.

from django.http import JsonResponse
from rest_framework.views import APIView
#from rest_framework.response import Response
from .serializers import SellerSerializer
from .models import User

class SellerView(APIView):
    """
    Seller View
    """

    def get(self, request, format=None):
        strn = "Get method "+str(User.id)
        print ("-----")
        #print (User.objects.values_list().filter(email='s'))
        #print (User.objects.filter(email='s@gmail.com').first())
        print (request.user)
        data = {'message': strn}
        sellerResponse = SellerSerializer(data)
        return JsonResponse(sellerResponse.data)

    def post(self, request, format=None):
        data = {'message': 'Post method'}
        sellerResponse = SellerSerializer(data)
        return JsonResponse(sellerResponse.data)
