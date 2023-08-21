from django.db import models

from user_auth.models import BoltUser

from .constants import DISTANCE_INDEX, PRICE_AND_DISTANCE, PRICE_INDEX


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


class Ticket(models.Model):
    """Describe instance of ticket."""
    MAX_LENGTH = {
        'ORIGIN': 30,
        'DESTINATION': 30,
        'UNIQUE_NUMBER': 60
    }
    image = models.ImageField(upload_to='images/')
    origin = models.CharField(verbose_name='Origin', max_length=MAX_LENGTH['ORIGIN'], blank=True, null=True)
    destination = models.CharField(verbose_name='Destination', max_length=MAX_LENGTH['DESTINATION'], blank=True, null=True)
    unique_number = models.CharField(verbose_name='Unique number', max_length=MAX_LENGTH['UNIQUE_NUMBER'], unique=True, null=True)
    user = models.ForeignKey(BoltUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
