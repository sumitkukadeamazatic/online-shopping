"""
Return APP urls
"""
from rest_framework import routers
from .views import ReturnViewSet

ROUTER = routers.SimpleRouter()
ROUTER.register(r'', ReturnViewSet, base_name='return')
urlpatterns = ROUTER.urls
