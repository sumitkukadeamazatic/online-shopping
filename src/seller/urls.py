"""
Seller App Urls
"""

from rest_framework import routers
from .views import SellerViewSet, ChangeStatusViewSet

router = routers.DefaultRouter()
router.register(r'change-status', ChangeStatusViewSet, base_name='change-status')
router.register(r'', SellerViewSet, base_name='seller')
urlpatterns = router.urls
