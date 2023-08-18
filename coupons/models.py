from django.db import models

from user_auth.models import BoltUser
from .constants import PRICE_AND_DISTANCE, PRICE_INDEX, DISTANCE_INDEX


class Coupon(models.Model):
    """Describe instance of coupon."""
    MAX_LENGTH = {
        'NAME': 8, 
    }

    name = models.CharField(verbose_name='coupon', unique=True, max_length=MAX_LENGTH['NAME'])
    price = models.PositiveIntegerField(verbose_name='price', default=PRICE_AND_DISTANCE[0][PRICE_INDEX])
    distance = models.PositiveIntegerField(verbose_name='distance', default=PRICE_AND_DISTANCE[0][DISTANCE_INDEX])
    expiration_date = models.DateField(verbose_name='expiration date', auto_now_add=False, auto_created=False)
    user = models.ForeignKey(BoltUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.name} Distance: {self.distance} Price: {self.price} Expired at: {self.expiration_date}'
