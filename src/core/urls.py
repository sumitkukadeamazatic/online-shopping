"""
     Application's core urls
"""
from user.views import UserLoginView
from django.contrib import admin
from django.urls import path, include
from knox import views as knox_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('product/', include('product.urls')),
    path('review/', include('product.urls')),
    path('address/', include('contact.urls')),
    path('cart/', include('order.urls')),
    path('api/auth/login', UserLoginView.as_view()),
    path('api/auth/logout', knox_views.LogoutView.as_view()),
    path('api/auth/logoutall', knox_views.LogoutAllView.as_view()),
    path('wishlist/', include('product.wishlist-urls')),
    path('offer/', include('offer.urls')),
    path('order/', include('order.order_urls')),
]
