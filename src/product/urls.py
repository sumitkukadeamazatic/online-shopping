"""
    User App URLs
"""

from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('/wishlist', WishlistViewset, base_name='wishlist')
urlpatterns = router.urls

urlpatterns = [
    #path('auth', LoginView.as_view()),
    #path('authorization-test', AuthenticateTest.as_view()),
    #path('second-test', SecondTestView.as_view()),
    #path('third-test', ThirdTestView.as_view())
    path('category', CategoryView.as_view())
]
