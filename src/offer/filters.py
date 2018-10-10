"""
Offer App Filters
"""

from rest_framework.filters import BaseFilterBackend
from django.utils import timezone
from .models import Offer


class OfferFilterBackend(BaseFilterBackend):
    """
    Custom filter backend for Offers
    """

    def filter_queryset(self, request, queryset, view):
        today = timezone.localdate()
        queryset = Offer.objects.filter(valid_upto__gte=today)
        if 'product' in request.GET:
            queryset = queryset.filter(
                productoffer__product_id=request.GET['product'])
        return queryset
