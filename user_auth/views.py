"""Views for user_auth app."""
from django.contrib.auth import authenticate
from django.http import HttpRequest, HttpResponse
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializers import UserLoginSerializer, UserRegistrationSerializer


class UserLoginView(generics.CreateAPIView):
    """Login view."""
    serializer_class = UserLoginSerializer

    def create(self, request: HttpRequest) -> HttpResponse:
        """
        Create JWT token.
        
        :param request: http request.
        :return: response -> 200 {"token": "token"}
                 response -> 400 when field is empty or invalid
                 response -> 401 {"detail": "Invalid credentials"}
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserRegistrationView(generics.CreateAPIView):
    """Registration view."""
    serializer_class = UserRegistrationSerializer
