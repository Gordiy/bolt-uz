import os

from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_400_BAD_REQUEST

from user_auth.models import BoltUser
from rest_framework.authtoken.models import Token


def register_social_user(request, email):
    filtered_user_by_email = BoltUser.objects.filter(email=email)

    if filtered_user_by_email.exists():
        registered_user = authenticate(
            request=request, username=email, password=os.environ.get('SOCIAL_SECRET', 'social_secret'))
        
        if not registered_user:
            raise ValidationError(detail='Login with email and password.', code=HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=registered_user)
        return {'token': token.key}

    else:
        user = {
            'username': email, 'email': email,
            'password': os.environ.get('SOCIAL_SECRET', 'social_secret')}
        user = BoltUser.objects.create_user(**user)
        user.is_verified = True
        user.save()

        new_user = authenticate(
            username=email, password=os.environ.get('SOCIAL_SECRET', 'social_secret'))
        
        token, created = Token.objects.get_or_create(user=new_user)
        return {'token': token.key}
