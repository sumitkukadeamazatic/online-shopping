"""
   Contact App Views
"""
from contact.models import Address
from contact.serializers import AddressSerializer
from rest_framework import viewsets

class AddressViewset(viewsets.ModelViewSet):
    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Address.objects.filter(user=user)

    serializer_class = AddressSerializer
