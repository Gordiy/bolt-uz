from rest_framework import serializers

from .models import Coupon, Ticket


class CouponSerializer(serializers.ModelSerializer):
    """Coupon serializer."""
    class Meta:
        model = Coupon
        fields = ('id', 'name', 'price')


class TicketImageSerializer(serializers.ModelSerializer):
    """Ticket image serializer."""
    class Meta:
        model = Ticket
        fields = ['image']
