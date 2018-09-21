"""
Return App Views
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from .serializers import ReturnLineitemShippingSerializer, ReturnSerializer, ReturnSerializer, ViewReturnSerializer
import json


class ReturnViewSet(viewsets.ModelViewSet):
    """
        A viewset to create and list return order using ModelViewSet
    """

    def get_queryset(self):
        cart_ids = Cart.objects.filter(
            user_id=self.request.user.id).values_list('id', flat=True)
        order_ids = Order.objects.filter(
            cart_id__in=cart_ids).values_list('id', flat=True)
        returnOrder_ids = ReturnOrder.objects.filter(
            order_id__in=order_ids).values_list('id', flat=True)
        returnLineitem_ids = ReturnLineitem.objects.filter(
            return_order_id__in=returnOrder_ids)
        return returnLineitem_ids

    def get_serializer_class(self):
        if self.action == 'create':
            return ReturnSerializer
        else:
            return ViewReturnSerializer

    @action(detail=False, methods=['post'], url_path='lineitem-shipping-detail')
    def create_lineitem_shipping_detail(self, request):
        """
        Save shipping details and corrensponding return lineitems
        """
        lineitems = request.data.pop('return_lineitems')
        shipping_details = request.data
        lineitem_shippingdetails_serializer = ReturnLineitemShippingSerializer(
            data={'shipping_details': shipping_details, 'lineitems': lineitems})
        lineitem_shippingdetails_serializer.is_valid(raise_exception=True)
        response = lineitem_shippingdetails_serializer.save()
        return Response(response['response'], status=HTTP_201_CREATED)
