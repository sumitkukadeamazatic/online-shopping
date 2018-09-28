"""
   Contact App Views
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from contact.models import Address
from contact.serializers import AddressSerializer

class AddressViewset(viewsets.ModelViewSet): #pylint: disable=too-many-ancestors
    """
        this viewset class is used to adress API
    """
    serializer_class = AddressSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
            this queset return filter user Address
        """
        return Address.objects.filter(user=self.request.user)
