"""
Seller App Urls
"""

#from rest_framework import routers
#from .views import SellerViewSet
from .views import SellerView
from django.urls import path

urlpatterns = [
            path('add-seller',SellerView.as_view())
]

'''
router = routers.SimpleRouter()
router.register(r'', SellerViewSet, base_name='seller')
urlpatterns = router.urls
'''
