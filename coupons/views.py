"""Views for coupons app."""
from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet

from .models import Coupon
from .serializers import CouponSerializer, TicketImageSerializer
from .services import (CalculateDistanceService, CouponService,
                       StationRecognitionService)


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

        user.update_distance(-coupon.distance)

        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def upload_ticket(self, request: HttpRequest) -> HttpResponse:
        """
        Upload ticket.
        
        :param request: http request.
        :return: http response.
        """
        serializer = TicketImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        station_recognition_service = StationRecognitionService(serializer.validated_data.get('image'))
        result = station_recognition_service.recognite()
        try:
            origin = result.get('origin').lower()
            destination = result.get('destination').lower()
        except IndexError:
            raise ValidationError(detail='Settlements are not recognized.', code=HTTP_400_BAD_REQUEST)

        distance = CalculateDistanceService().calculate_distance(origin, destination)
        user = request.user
        
        station_recognition_service.save_ticket(origin, destination, result.get('ticket_number'), user)
        user.update_distance(distance)

        return Response(data={'distance': distance})
