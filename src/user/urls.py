"""
    User App URLs
"""

from rest_framework import routers
from .views import (UserViewSet)


ROUTER = routers.SimpleRouter()
ROUTER.register(r'', UserViewSet)
urlpatterns = ROUTER.urls
