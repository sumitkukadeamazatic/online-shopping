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
        queryset = Offer.objects.filter(
            valid_from__lte=today, valid_upto__gte=today)
        if 'product' in request.GET:
            current_offer_id = queryset.only('id')
            queryset = Offer.objects.filter(
                id__in=current_offer_id, productoffer__product_id=request.GET['product'])
        return queryset
