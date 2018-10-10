"""
    this url file used to cart API url
"""
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter() #pylint: disable=invalid-name
router.register(r'(?P<cart>\d+)/cartproduct', views.CartProductViewset, base_name='cartproduct')
urlpatterns = router.urls
