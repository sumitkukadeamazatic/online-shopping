"""
Seller App Urls
"""

from rest_framework import routers
from .views import SellerViewSet

router = routers.DefaultRouter()
router.register(r'', SellerViewSet, base_name='seller')
urlpatterns = router.urls
