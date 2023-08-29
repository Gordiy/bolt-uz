"""Serializer for user_auth app."""
import os

from django.contrib.auth.models import AbstractUser
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .models import BoltUser
from .social.facebook import Facebook
from .social.google import Google
from .social.register import register_social_user


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for registering users."""
    class Meta:
        model = BoltUser
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data: dict) -> AbstractUser:
        """
        Create user instance.
        Store username as email.

        :param validated_data: validated data.
        :return: user instance.
        """
        return BoltUser.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            username=validated_data['email'],  # Use email as username
            password=validated_data['password']
        )


class UserLoginSerializer(serializers.Serializer):
    """Serializer for logged in users."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class FacebookSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of facebook related data"""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = Facebook.validate(auth_token)

        try:
            email = user_data['email']
            return register_social_user(email=email)
        except Exception:
            raise serializers.ValidationError(
                'The token  is invalid or expired. Please login again.'
            )


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        print(f'USER DATA: {user_data} \n')
        print(f'GOOGLE_SOCIAL_AUTH_CLIENT_ID: {os.environ.get("OOGLE_SOCIAL_AUTH_CLIENT_ID")}')
        if user_data['aud'] != os.environ.get('GOOGLE_SOCIAL_AUTH_CLIENT_ID'):
            raise AuthenticationFailed('oops, who are you?')

        email = user_data['email']

        return register_social_user(request=self.context.get('request'), email=email)
