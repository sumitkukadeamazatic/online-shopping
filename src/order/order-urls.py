from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('', views.OrderViewset, base_name='order')
router.register('tax', views.TaxViewset, base_name='tax')
router.register('tax-invoice', views.TaxInvoiceViewset, base_name='tax-invoice')
urlpatterns = router.urls
