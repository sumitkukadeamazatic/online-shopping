from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('', views.AddressViewset, base_name='todos')
urlpatterns = router.urls