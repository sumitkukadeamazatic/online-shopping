from rest_framework import viewsets, status
from .models import Order
from .serializers import *
from rest_framework.response import Response

class ReturnViewSet(viewsets.ViewSet):
    """
        A ViewSet to create and list return order
    """

    # queryset = Order.objects.all()
    # serializer_class = ReturnSerializer

    def list(self, request):
        queryset = Order.objects.all()
        serializer = ReturnSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        if not Order.objects.filter(order_id=request.data['order']):
            return_order_serializer = ReturnSerializer(data=request.data)
            if return_order_serializer.is_valid():
                return_order_serializer.save()
        serializer = ReturnLineitemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
