"""
     Seller App Views
"""

from .serializers import *
from .models import SellerUser, Seller, User
from product.models import Review
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class SellerViewSet(viewsets.ModelViewSet):
    """
        Seller View using Model Viewset
    """

    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    #permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        print (self.action)
        if self.action == 'retrieve':
            return SellerDetailSerializer
        else:
            return SellerSerializer
