from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^(?P<pk>[0-9]+)/$', views.AddressList.as_view(), name='AddressView'),
]