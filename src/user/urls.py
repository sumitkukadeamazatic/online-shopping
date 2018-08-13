"""
    User App URLs
"""


from django.urls import path
from .views import *

urlpatterns = [
    path('login', login),
    path('authorization-test', AuthenticateTest.as_view())
]
