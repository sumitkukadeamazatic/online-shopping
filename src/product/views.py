"""
product app models
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, authentication, viewsets
from django.http import Http404#, JsonResponse
# from django.shortcuts import render

from django.core.paginator import Paginator
#from .serializers import CategorySerializer
from .models import Category, Product, ProductSeller, Review, ProductFeature, Feature, User
from seller.models import Seller, SellerUser
from .models import Category, Wishlist
from rest_framework import viewsets, status
from rest_framework.response import Response
from .permissions import UserAccessPermission
from .serializers import (WishlistSerializer,
                          WishlistPostSerializer,
                          ReviewPostSerializer,
                          CategorySerializer,
                          ReviewSerializer,
                          ProductSerializer)

class WishlistViewset(viewsets.ModelViewSet):

    def get_queryset(self):
        """
        This view should return a list of all the Address
        for the currently authenticated user.
        """
        user = self.request.user
        return Wishlist.objects.filter(user=user)

    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [UserAccessPermission]
    serializer_class = WishlistSerializer

    def get_paginated_response(self, data):
        return Response(data)

class CategoryView(viewsets.ModelViewSet):
    '''
    category view -
    view to list all category to the db
    Anyone can access the view
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)


class ProductView(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)


class ProductSellerView(viewsets.ModelViewSet):
    queryset = Product.objects.all()


class ReviewView(viewsets.ModelViewSet):
    def list(self, request):
        seller_id = request.GET.get('seller_id', False)
        product_id = request.GET.get('product_id', False)
        # if seller_id and product_id is not given or both given
        if not (bool(seller_id) ^ bool(product_id)):
            return Response({"response":"Invalid Request."})

        if seller_id:
            queryset = Review.objects.filter(seller=seller_id)
        if product_id:
            queryset = Review.objects.filter(product=product_id)

        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        data['user'] = request.user.id
        try:
            if not (bool(data['seller']) ^ bool(data['product'])):
                return Response({"response":"Invalid Request."})
        except KeyError:
            return Response({"response":"Mandatory field(s) missing."})

        serializer = ReviewPostSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({})

    def partial_update(self, request, pk=None):
        data = request.data
        data['user'] = request.user.id
        try:
            if not (bool(data['seller']) ^ bool(data['product'])):
                return Response({"response":"Invalid Request."})
        except KeyError:
            return Response({"response":"Mandatory field(s) missing."})
        
        serializer = ReviewPostSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
