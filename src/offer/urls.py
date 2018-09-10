"""
    Offer App URLs
"""

from rest_framework import routers
from .views import (OfferViewSet)


ROUTER = routers.SimpleRouter()
ROUTER.register(r'', OfferViewSet)
urlpatterns = ROUTER.urls
