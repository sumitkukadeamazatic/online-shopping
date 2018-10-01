"""
    this urls file used to address api urls
"""
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter() #pylint: disable=invalid-name
router.register('', views.AddressViewset, base_name='todos')
urlpatterns = router.urls
