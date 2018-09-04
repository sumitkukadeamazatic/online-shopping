"""
   Contact App Views
"""
from contact.models import Address
from contact.serializers import AddressSerializer
from rest_framework import viewsets
from rest_framework.response import Response


class AddressViewset(viewsets.ModelViewSet):
    def get_queryset(self):
        """
        This view should return a list of all the Address
        for the currently authenticated user.
        """
        user = self.request.user
        return Address.objects.filter(user=user)

    serializer_class = AddressSerializer

    def get_paginated_response(self, data):
       return Response(data)