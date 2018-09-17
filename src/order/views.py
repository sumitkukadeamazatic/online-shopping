"""
   Contact App Views
"""
from order.models import Cart, CartProduct, Order
from order.serializers import  CartProductSerializer, AddCartProductSerializer, OrderSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from .permissions import UserAccessPermission

class OrderViewset(viewsets.ViewSet):

    def get_queryset(self):
        """
        This view should return a list of all the Address
        for the currently authenticated user.
        """
        user = self.request.user
        return Order.objects.filter(cart=Cart.objects.get_or_create(user=user,is_cart_processed=False)[0])

    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [UserAccessPermission]
    serializer_class = OrderSerializer

    def get_paginated_response(self, data):
       return Response(data)


class CartViewset(viewsets.ModelViewSet):
    
    def get_serializer_class(self):
        if self.request.method != 'POST':
            return CartProductSerializer
        return AddCartProductSerializer

    def get_queryset(self):
        """
        This view should return a list of all the Address
        for the currently authenticated user.
        """
        user = self.request.user
        return CartProduct.objects.filter(cart=Cart.objects.get_or_create(user=user,is_cart_processed=False)[0])

    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [UserAccessPermission]
    

    def get_paginated_response(self, data):
       return Response(data)