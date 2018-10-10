"""
    This url file is use to ordderAPI urls
"""
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()  #pylint: disable=invalid-name
router.register(r'tax-invoice', views.TaxInvoiceViewset, base_name='tax-invoice')
router.register(r'tax', views.TaxViewset, base_name='tax')
router.register(r'shipping', views.OrderShippingViewset, base_name='shipping')
router.register(r'payment-method', views.PaymentMethodViewset, base_name='payment-method')
router.register(r'', views.OrderViewset, base_name='order')
urlpatterns = router.urls
