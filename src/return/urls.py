"""
Return APP urls
"""
from rest_framework import routers
from .views import ReturnViewSet

router = routers.SimpleRouter()
router.register(r'', ReturnViewSet, base_name='return')
urlpatterns = router.urls
