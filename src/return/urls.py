"""
Return APP urls
"""

from django.urls import path
from .views import ReturnLineItemShippingView

urlpatterns = [
    path('lineitem-shipping-detail', ReturnLineItemShippingView.as_view())
]
