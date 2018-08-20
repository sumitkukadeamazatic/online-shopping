"""
    User App URLs
"""

from rest_framework import routers
from django.urls import path
from .views import (UserViewSet, request_forgot_password)


router = routers.SimpleRouter()
router.register(r'', UserViewSet)
urlpatterns = router.urls
