"""
    this urls file is used to wishlist urls
"""
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter() #pylint: disable=invalid-name
router.register(r'', views.WishlistViewset, base_name='wishlist')
urlpatterns = router.urls
