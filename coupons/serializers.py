from rest_framework import serializers

from .models import Coupon, Ticket


class CouponSerializer(serializers.ModelSerializer):
    """Coupon serializer."""
    class Meta:
        model = Coupon
        fields = ('id', 'name', 'price')


class TickeUploadFiletSerializer(serializers.ModelSerializer):
    """Ticket upload file serializer."""
    class Meta:
        model = Ticket
        fields = ['file']


class TicketSerializer(serializers.ModelSerializer):
    """Ticket serializer."""
    class Meta:
        model = Ticket
        fields = ['id', 'origin', 'destination']
