"""Urls for user_auth app."""
from django.urls import path

from .views import UserLoginView, UserRegistrationView, FacebookSocialAuthView, GoogleSocialAuthView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('facebook/', FacebookSocialAuthView.as_view(), name='facebook'),
    path('google/', GoogleSocialAuthView.as_view(), name='google')
]
