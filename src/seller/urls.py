"""
Seller App Urls
"""

from django.urls import path
from .views import *

urlpatterns = [
            path('seller',SellerView.as_view())
        ]
