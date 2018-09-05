"""
   Contact App Views
"""
from order.models import Cart, CartProduct
from order.serializers import  CartProductSerializer, CartProductPostSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response


class CartViewset(viewsets.ViewSet):

    def list(self, request):
        user = self.request.user
        queryset = CartProduct.objects.filter(cart=Cart.objects.get(user=user,is_cart_processed=False))
        serializer = CartProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        user = self.request.user
        cp = CartProduct.objects.get(cart=Cart.objects.get(user=user,is_cart_processed=False),pk=pk)
        serializer = CartProductSerializer(cp,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'Error':'Not valid data'})

    def create(self, request):
        data = {}
        user = self.request.user
        cart=Cart.objects.get(user=user,is_cart_processed=False)
        data['quantity'] = request.data['quantity']
        data['product_seller'] = request.data['product_seller']
        data['is_order_generated'] = False
        data['cart'] = cart.id
        serializer = CartProductPostSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def destroy(self, request, pk=None):
        res = CartProduct.objects.get(pk=pk,cart=Cart.objects.get(user=self.request.user,is_cart_processed=False)).delete()
        return Response({"Msage":"deleted  sussesfully"},status=status.HTTP_204_NO_CONTENT)
