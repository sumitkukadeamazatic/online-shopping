"""
     Seller App Views
"""
# from django.shortcuts import render
# Create your views here.

#from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from .serializers import SellerSerializer
from .models import User,Seller

class SellerView(APIView):

    def get(self, request, format=None):
        print ("-----")
        #print (User.objects.values_list().filter(email='s'))
        #print (User.objects.filter(email='s@gmail.com').first())
        print (request.data)
        data = {'message': 'Get method'}
        sellerResponse = SellerSerializer(data)
        return JsonResponse(sellerResponse.data)

    def post(self, request, format=None):
        print (request.data)
#        print (request.META)
        print (request.META.get('HTTP_TOKEN'))
        data = {'message': 'Post method'}
        sellerResponse = SellerSerializer(data)
        return JsonResponse(sellerResponse.data)

'''
class SellerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Seller View
    """

    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = (permissions.AllowAny,)

    def list(self,request):
        print(request.data)
        data = {'message':'list method'}
        sellerResponse = SellerSerializer(data)
        return JsonResponse(sellerResponse.data)

    def create(self, request):
        print (request.data)
        data = {'message':'create method'}
        sellerResponse = SellerSerializer(data)
        return JsonResponse(sellerResponse.data)
'''
