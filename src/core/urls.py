from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('product/', include('product.urls')),
    path('address/', include('contact.urls')),
    path('cart/', include('order.urls')),
    path('wishlist/', include('product.wishlist-urls')),
]
