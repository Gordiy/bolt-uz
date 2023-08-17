"""Serializer for user_auth app."""
from django.contrib.auth.models import AbstractUser
from rest_framework import serializers

from .models import BoltUser


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
        return  BoltUser.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            username=validated_data['email'],  # Use email as username
            password=validated_data['password']
        )
