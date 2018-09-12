from rest_framework import viewsets, status
from .models import Order as ReturnOrder
from order.models import *
from .serializers import *
from rest_framework.response import Response

class ReturnViewSetPrevious(viewsets.ViewSet):
    """
        A ViewSet to create and list return order
    """

    # queryset = Order.objects.all()
    # serializer_class = ReturnSerializer

    def list(self, request):
        queryset = Order.objects.all()
        serializer = ReturnSerializer(queryset, many=True)
        return Response(serializer.data)

    """
    def create(self, request):
        if not ReturnOrder.objects.filter(order_id=request.data['order']):
            returnOrder_serializer = ReturnOrderSerializer(data=request.data)
            if returnOrder_serializer.is_valid():
                returnOrder_serializer.save()
                return Response(returnOrder_serializer.data, status=status.HTTP_201_CREATED)
            return Response(returnOrder_serializer.errors)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    """

    def create(self, request):
        serializer = ReturnLineitemSerializer(data=request.data, context = request.data) # context = {'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

class ReturnViewSet(viewsets.ModelViewSet):
    """
        A viewset to create and list return order
    """

    queryset = ReturnOrder.objects.all()
    serializer_class = ViewReturnSerializer

    def get_queryset(self):
        # print (ReturnLineitem.objects.filter(return_order_id=13))
        # return ReturnLineitem.objects.filter(return_order_id=13)
        cart_ids = Cart.objects.filter(user_id=self.request.user.id).values_list('id', flat=True)
        # print (cart_ids)
        order_ids = Order.objects.filter(cart_id__in=cart_ids).values_list('id', flat=True)
        # print (order_ids)
        returnOrder_ids = ReturnOrder.objects.filter(order_id__in=order_ids).values_list('id',flat=True)
        # print (returnOrder_ids)
        returnLineitem_ids = ReturnLineitem.objects.filter(return_order_id__in=returnOrder_ids)
        # print (returnLineitem_ids)
        # print (ReturnLineitem.objects.all().count())
        return returnOrder_ids

'''
    def get_paginated_response(self, obj):
        return Response(obj)
'''
