"""
    Offer app views
"""

from rest_framework import viewsets
from rest_framework.response import Response
from .models import Offer
from .filters import OfferFilterBackend
from .serializers import OfferSerializer


class OfferViewSet(viewsets.ModelViewSet):
    """
        Offer related views
    """
    queryset = Offer.objects.all()
    filter_backends = (OfferFilterBackend,)
    serializer_class = OfferSerializer
