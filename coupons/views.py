"""Views for coupons app."""
from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import action
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Coupon
from .serializers import CouponSerializer
from .services import CouponService
from user_auth.services import BoltUserService


class CouponViewSet(DestroyModelMixin, GenericViewSet):
    """Viewset retrieve coupon for user and delete coupon."""
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated | IsAdminUser]

    @action(detail=False, methods=['GET'])
    def get(self, request: HttpRequest, pk=None) -> HttpResponse:
        """
        Retrieve coupon by user distance.
        
        :param request: http request.
        :return: response.
        """
        user = request.user
        coupon = CouponService().get_coupon_by_distance(user)
        serializer = self.serializer_class(coupon)

        BoltUserService.update_user_distance(user, coupon.distance)

        return Response(serializer.data)
