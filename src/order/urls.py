from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('', views.CartViewset, base_name='cart')
urlpatterns = router.urls
