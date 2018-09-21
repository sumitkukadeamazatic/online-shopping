"""
    Product App URLs
"""

from django.urls import path
from .views import (CategoryView,
                    ProductView,
                    ProductSellerView,
                    SellerReviewView,
                    #ProductReviewView,
                    WishlistViewset)
                    #ReviewView)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('wishlist', WishlistViewset, base_name='wishlist')
router.register('sellers', ProductSellerView, base_name='sellers')
router.register('category', CategoryView, base_name='category')
router.register('review/seller', SellerReviewView, base_name='review')
router.register('', ProductView, base_name='product')
urlpatterns = router.urls

