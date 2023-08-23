"""Models for auth app."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class BoltUser(AbstractUser):
    """Describe Bolt User instance."""
    MAX_LENGTH = {
        'FIRST_NAME': 35,
        'LAST_NAME': 35,
    }

    first_name = models.CharField(max_length=MAX_LENGTH['FIRST_NAME'])
    last_name = models.CharField(max_length=MAX_LENGTH['LAST_NAME'])
    email = models.EmailField(unique=True)
    distance = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        """String representation of user instance."""
        return f'{self.first_name} {self.last_name}'
    
    def update_distance(self, distance: str):
        """
        Update user distance.
        
        :param distance: coupon distance.
        :return: None.
        """
        self.distance = self.distance + distance
        self.save()
