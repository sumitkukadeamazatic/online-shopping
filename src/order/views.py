"""
   Contact App Views
"""
from order.models import Cart, CartProduct
from order.serializers import CartSerializer
from rest_framework import viewsets

class CartViewset(viewsets.ModelViewSet):
    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        cart = Cart.objects.get(user=user, is_cart_processed=False)
        return CartProduct.objects.filter(cart=cart)

    serializer_class = CartSerializer