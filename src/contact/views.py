"""
   Contact App Views
"""
from contact.models import Address
from contact.serializers import AddressSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from .permissions import UserAccessPermission

class AddressViewset(viewsets.ModelViewSet):
    
    serializer_class = AddressSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = [UserAccessPermission]

    def get_queryset(self):
        """
        This view should return a list of all the Address
        for the currently authenticated user.
        """
        user = self.request.user
        return Address.objects.filter(user=user)
        
    def get_paginated_response(self, data):
       return Response(data)