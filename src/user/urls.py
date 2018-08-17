"""
    User App URLs
"""

from django.urls import path, re_path
from rest_framework import routers
from .views import (UserViewSet)


router = routers.SimpleRouter()
router.register(r'', UserViewSet)
urlpatterns = router.urls
