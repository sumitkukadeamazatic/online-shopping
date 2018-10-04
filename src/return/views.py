"""
Return App Views
"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from .models import Order as ReturnOrder
from .permissions import ReturnAccessPermission
from .serializers import ReturnLineitemShippingSerializer, ViewReturnSerializer, ReturnLineitemSerializer


class ReturnViewSet(viewsets.ModelViewSet):  # pylint: disable=too-many-ancestors
    """
        A viewset to create and list return order using ModelViewSet
    """

    permission_classes = (ReturnAccessPermission,)

    def list(self, request, *args, **kwargs):
        return_orders = ReturnOrder.objects.filter(
            order__cart__user=request.user).values('id', 'status', 'order_id', 'created_at')
        return_serializer = ViewReturnSerializer(
            data=list(return_orders), many=True)
        return_serializer.is_valid(raise_exception=True)
        self.paginate_queryset(return_serializer.data)
        return super(ReturnViewSet, self).get_paginated_response(return_serializer.data)

    def create(self, request, *args, **kwargs):
        lineitem_serializer = ReturnLineitemSerializer(data=request.data)
        lineitem_serializer.is_valid(raise_exception=True)
        response_data = lineitem_serializer.save()
        return Response(response_data, status=HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='lineitem-shipping-detail')
    def create_lineitem_shipping_detail(self, request):  # pylint: disable=no-self-use
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
