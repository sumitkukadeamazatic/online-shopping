"""
   Contact App Views
"""
from order.models import Cart, CartProduct, Order, Lineitem
from product.models import CategoryTax
from order.serializers import  (CartProductSerializer,
                                AddCartProductSerializer,
                                TaxInvoiceSerializer,
                                OrderSerializer,
                                TaxSerializer)
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
