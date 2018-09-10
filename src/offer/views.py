"""
    Offer app views
"""

from rest_framework import viewsets
from .models import Offer
from .filters import OfferFilterBackend
from .serializers import OfferSerializer


class OfferViewSet(viewsets.ModelViewSet):  # pylint: disable=too-many-ancestors
    """
        Offer related views
    """
    queryset = Offer.objects.all()
    filter_backends = (OfferFilterBackend,)
    serializer_class = OfferSerializer
