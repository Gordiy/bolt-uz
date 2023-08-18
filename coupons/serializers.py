from rest_framework import serializers

from .models import Coupon


class CouponSerializer(serializers.ModelSerializer):
    """Coupon serializer."""
    class Meta:
        model = Coupon
        fields = ('id', 'name', 'price')
