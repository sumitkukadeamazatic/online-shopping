"""
    User App URLs
"""

from django.urls import path, re_path
from .views import (LoginView, UserView)

urlpatterns = [
    path('', UserView.as_view()),
    path('<int:id>', UserView.as_view()),
    path('auth', LoginView.as_view()),
]
