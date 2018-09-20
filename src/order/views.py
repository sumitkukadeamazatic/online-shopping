"""
   Contact App Views
"""
from order.models import Cart, CartProduct, Order, Lineitem, ShippingDetails
from product.models import CategoryTax
from order.serializers import  (CartProductSerializer,
                                TaxInvoiceSerializer,
                                OrderSerializer,
                                OrderShippingSerializer,
                                TaxSerializer)
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
        return Order.objects.filter(cart__user=self.request.user)
    
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
        return CartProduct.objects.filter(cart=Cart.objects.get_or_create(user = self.request.user,is_cart_processed=False)[0])


    def get_paginated_response(self, data):
        return Response(data)

class TaxViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes = [UserAccessPermission]
    queryset = CategoryTax.objects.all()
    serializer_class = TaxSerializer
        
    

    def retrieve(self, request, pk=None):
        queryset = CategoryTax.objects.filter(category = pk)
        serializer_class = TaxSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def get_paginated_response(self, data):
        return Response(data)

class ShippingViewset(viewsets.ModelViewSet):
    def create(self, request):
        print(request.data)
        return Response({})

class TaxInvoiceViewset(viewsets.ReadOnlyModelViewSet):
    def retrieve(self, request, pk=None):
        queryset = Lineitem.objects.filter(order=pk)
        serializer_class = TaxInvoiceSerializer(queryset, many=False)
        return Response(serializer_class.data)

class OrderShippingViewset(viewsets.ModelViewSet):
    permission_classes = (UserAccessPermission,)
    serializer_class = OrderShippingSerializer
    queryset = ShippingDetails.objects.all()