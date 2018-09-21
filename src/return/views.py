from rest_framework import viewsets, status
from .models import Order as ReturnOrder
from order.models import *
from .serializers import *
from rest_framework.response import Response
import json

class ReturnViewSetPrevious(viewsets.ViewSet):
    """
        A ViewSet to create and list return order using Viewset
    """

    def list(self, request):
        queryset = Order.objects.all()
        serializer = ReturnSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ReturnLineitemSerializer(data=request.data, context = request.data) # context = {'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class ReturnViewSet(viewsets.ModelViewSet):
    """
        A viewset to create and list return order using ModelViewSet
    """

    def get_queryset(self):
        cart_ids = Cart.objects.filter(user_id=self.request.user.id).values_list('id', flat=True)
        order_ids = Order.objects.filter(cart_id__in=cart_ids).values_list('id', flat=True)
        returnOrder_ids = ReturnOrder.objects.filter(order_id__in=order_ids).values_list('id',flat=True)
        # returnOrder_ids = ReturnOrder.objects.filter(order_id__in=order_ids)
        returnLineitem_ids = ReturnLineitem.objects.filter(return_order_id__in=returnOrder_ids)
        return returnLineitem_ids

    def get_serializer_class(self):
        if self.action == 'create':
            # json_data = json.loads(request.body)
            # print (json_data)
            return ReturnSerializer
        else:
            return ViewReturnSerializer

'''
    def get_paginated_response(self, obj):
        return Response(obj)
'''
