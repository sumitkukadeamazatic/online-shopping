"""
   Contact App Views
"""
from contact.models import Address
from contact.serializers import AddressSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class AddressList(APIView):
    """
    Address Vies is use to Create, Update, Delete adresses
    """
    def get(self, request, format=None):
        address = None
        if request.GET.get('flag'):
            address = Address.objects.filter(user_id = request.GET.get('id')).order_by('id')
        else:
            address = Address.objects.filter(seller_id = request.GET.get('id')).order_by('id')
        serializer = AddressSerializer(address, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, format=None):
        address = Address.objects.get(pk=request.data['id'])
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        print(request.data['id'])
        address = Address.objects.get(pk=request.data['id'])
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)