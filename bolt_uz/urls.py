"""bolt_uz URL Configuration."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('auth/', include('user_auth.urls')),
    path('auth/social/', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls),
]
