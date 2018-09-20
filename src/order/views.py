"""
   Contact App Views
"""
from order.models import Cart, CartProduct, Order, Lineitem
from product.models import CategoryTax
from order.serializers import  (CartProductSerializer,
                                TaxInvoiceSerializer,
                                OrderSerializer,
                                TaxSerializer)
from rest_framework import viewsets, status
from rest_framework.response import Response
from .permissions import UserAccessPermission
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
import json


class OrderViewset(viewsets.ModelViewSet):
    
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = [UserAccessPermission]
    serializer_class = OrderSerializer

    def get_queyset(self):
        return   Order.objects.filter(cart__user=self.request.user)
    
    def get_paginated_response(self, data):
       return Response(data)

    @action(methods=['patch'], detail=True, permission_classes=[UserAccessPermission])
    def payment(self, request, pk=None):
        instance = self.get_object()
        instance.payment_info = json.loads(request.data['payment_info'])
        instance.save()
        return Response(OrderSerializer(instance).data)
 
    @action(methods=['post'], detail=False, permission_classes=[UserAccessPermission])
    def shipping(self, request):
        print("######################")
        #instance = self.get_object()
        #instance.payment_info = json.loads(request.data['payment_info'])
        #instance.save()
        return Response({})



class CartViewset(viewsets.ModelViewSet):
    
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = [UserAccessPermission]
    serializer_class = CartProductSerializer
    
    def get_queryset(self):
        user = self.request.user
        return CartProduct.objects.filter(cart=Cart.objects.get_or_create(user=user,is_cart_processed=False)[0])

    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [UserAccessPermission]

    def get_paginated_response(self, data):
        return Response(data)

class TaxViewset(viewsets.ReadOnlyModelViewSet):
    def list(self, request):
        queryset = CategoryTax.objects.all()
        serializer_class = TaxSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        queryset = CategoryTax.objects.filter(category = pk)
        serializer_class = TaxSerializer(queryset, many=True)
        return Response(serializer_class.data)

class ShippingViewset(viewsets.ModelViewSet):
    def create(self, request):
        print(request.data)
        return Response({})

class TaxInvoiceViewset(viewsets.ReadOnlyModelViewSet):
    def retrieve(self, request, pk=None):
        queryset = Lineitem.objects.filter(order=pk)
        serializer_class = TaxInvoiceSerializer(queryset, many=False)
        return Response(serializer_class.data)

    #def list(self, request):
        #return Response({})
#class OrderShippingViewset(viewsets.ModelViewSet):
    ##permission_classes = [UserAccessPermission]
    #def create(self, request):
        #return Response({})
        #queryser = 
