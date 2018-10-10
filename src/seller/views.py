"""
     Seller App Views
"""

from .serializers import *
from .models import SellerUser, Seller, User
from product.models import Review
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import SellerAccessPermission, ChangeStatusPermission

class SellerViewSet(viewsets.ModelViewSet):
    """
        Seller View to create, list and retrieve seller
    """

    permission_classes = [SellerAccessPermission]
    http_method_names = ('get','post','patch')

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Seller.objects.all()
        seller_id = SellerUser.objects.filter(user=self.request.user.id).values_list('seller', flat=True)
        return Seller.objects.filter(id__in=seller_id)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SellerDetailSerializer
        else:
            return SellerSerializer

class ChangeStatusViewSet(viewsets.ModelViewSet):
    """
        View to change status of seller
    """

    http_method_names = ('patch')
    queryset = Seller.objects.all()
    serializer_class = ChangeStatusSerializer
    permission_classes = [ChangeStatusPermission]
