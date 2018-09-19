"""
   Contact App Views
"""
from order.models import Cart, CartProduct, Order
from order.serializers import  CartProductSerializer, OrderSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from .permissions import UserAccessPermission
from rest_framework.decorators import action
import json


class OrderViewset(viewsets.ModelViewSet):
    
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = [UserAccessPermission]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(cart__in=Cart.objects.filter(user=user))
    
    def get_paginated_response(self, data):
       return Response(data)

    @action(methods=['patch'], detail=True, permission_classes=[UserAccessPermission])
    def payment(self, request, pk=None):
        instance = self.get_object()
        instance.payment_info = json.loads(request.data['payment_info'])
        instance.save()
        return Response(OrderSerializer(instance).data)


class CartViewset(viewsets.ModelViewSet):
    
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = [UserAccessPermission]
    serializer_class = CartProductSerializer
    
    def get_queryset(self):
        user = self.request.user
        return CartProduct.objects.filter(cart=Cart.objects.get_or_create(user=user,is_cart_processed=False)[0])

    def get_paginated_response(self, data):
       return Response(data)