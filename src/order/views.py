"""
   Contact App Views
"""
import json
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from product.models import CategoryTax
from .models import Cart, CartProduct, Order, Lineitem, ShippingDetails, PaymentMethod
from .serializers import CartProductSerializer, TaxInvoiceSerializer, OrderSerializer, OrderShippingSerializer, TaxSerializer, PaymentMethodSerializer  #pylint: disable=ungrouped-imports

class OrderViewset(viewsets.ModelViewSet):                  #pylint: disable=too-many-ancestors
    """
     OrderViewset is used to OrderAPI.
    """
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(cart__user=self.request.user)

    @action(methods=['patch'], detail=True, permission_classes=[IsAuthenticated])
    def payment(self, request, pk=None):    #pylint: disable=invalid-name
        """
            This method is used to the payment info.
        """
        instance = self.get_object()
        instance.payment_info = json.loads(request.data['payment_info'])
        instance.save()
        return Response(OrderSerializer(instance).data)


class CartViewset(viewsets.ModelViewSet):     #pylint: disable=too-many-ancestors
    """
     CartViewset is used to CartAPI.
    """
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = [IsAuthenticated]
    serializer_class = CartProductSerializer

    def get_queryset(self):
        return CartProduct.objects.filter(cart=Cart.objects.get_or_create(user=self.request.user, is_cart_processed=False)[0])


class TaxViewset(viewsets.ReadOnlyModelViewSet):    #pylint: disable=too-many-ancestors
    """
     TaxViewset is used to TaxAPI
    """
    permission_classes = [IsAuthenticated]
    queryset = CategoryTax.objects.all()
    serializer_class = TaxSerializer

    def retrieve(self, request, pk=None):         #pylint: disable=arguments-differ
        queryset = CategoryTax.objects.filter(category=pk)
        serializer_class = TaxSerializer(queryset, many=True)
        return Response(serializer_class.data)


class ShippingViewset(viewsets.ModelViewSet):     #pylint: disable=too-many-ancestors
    """
      ShippingViewset is used to ShippingAPI
    """
    def create(self, request):       #pylint: disable=arguments-differ
        print(request.data)
        return Response({})


class TaxInvoiceViewset(viewsets.ReadOnlyModelViewSet):     #pylint: disable=too-many-ancestors
    """
      TaxInvoiceViewset is used to TaxInvoiceAPI
    """
    def retrieve(self, request, pk=None):      #pylint: disable=arguments-differ
        queryset = Lineitem.objects.filter(order=pk)
        serializer_class = TaxInvoiceSerializer(queryset, many=False)
        return Response(serializer_class.data)


class OrderShippingViewset(viewsets.ModelViewSet):     #pylint: disable=too-many-ancestors
    """
      OrderShippingViewset is used to OrderShippingAPI
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderShippingSerializer
    queryset = ShippingDetails.objects.all()

class PaymentMethodViewset(viewsets.ReadOnlyModelViewSet):
    """
        Payment Method view used to display payment methods
    """

    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    permission_classes = (IsAuthenticated,)
