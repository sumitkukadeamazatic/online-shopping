"""
    Product App URLs
"""
from rest_framework.routers import DefaultRouter
from .views import (CategoryView,
                    ProductView,
                    ProductSellerView,
                    ProductReviewView,
                    SellerProductListingView,
                    SellerReviewView,
                    WishlistViewset)


router = DefaultRouter() #pylint: disable=invalid-name
router.register('listing', SellerProductListingView, base_name='seller-product')
router.register('', ProductView, base_name='product')
router.register('wishlist', WishlistViewset, base_name='wishlist')
router.register('sellers', ProductSellerView, base_name='sellers')
router.register('category', CategoryView, base_name='category')
router.register('review/seller', SellerReviewView, base_name='review')
router.register('review/product', ProductReviewView, base_name='review')
urlpatterns = router.urls
