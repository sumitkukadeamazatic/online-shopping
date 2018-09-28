"""
   Contact App Views
"""
from contact.models import Address
from contact.serializers import AddressSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class AddressViewset(viewsets.ModelViewSet):
    
    serializer_class = AddressSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
        
    def get_paginated_response(self, data):
       return Response(data)