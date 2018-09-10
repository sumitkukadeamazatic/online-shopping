from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('', views.OrderViewset, base_name='order')
urlpatterns = router.urls