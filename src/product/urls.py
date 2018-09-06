"""
    User App URLs
"""

from django.urls import path
from .views import CategoryView, ProductView, ProductSellerView, WishlistViewset
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('wishlist', WishlistViewset, base_name='wishlist')
urlpatterns = router.urls

urlpatterns += [
    path('category', CategoryView.as_view()),
    path('', ProductView.as_view()),
    path('<int:id>', ProductView.as_view()),
    path('product-seller', ProductSellerView.as_view()),
]
