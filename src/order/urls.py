"""
    this url file used to cart API url
"""
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter() #pylint: disable=invalid-name
router.register('', views.CartViewset, base_name='cart')
urlpatterns = router.urls
