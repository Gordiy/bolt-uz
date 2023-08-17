"""Urls for user_auth app."""
from django.urls import path

from .views import UserLoginView, UserRegistrationView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
]
