"""bolt_uz URL Configuration."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('auth/', include('user_auth.urls')),
    path('api/', include('coupons.urls')),
    path('admin/', admin.site.urls),
]
