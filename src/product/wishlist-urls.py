from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'',views.WishlistViewset, base_name='wishlist')
urlpatterns = router.urls