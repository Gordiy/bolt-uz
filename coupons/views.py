"""Views for coupons app."""
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet

from .models import Coupon
from .serializers import CouponSerializer, TicketSerializer
from .services import (CalculateDistanceService, CouponService,
                       ImageStationRecognitionService,
                       PDFStationRecognitionService)
from .utils import convert_to_temporary_uploaded_file, has_image_extension
from .constants import IMAGE_EXTENTSIONS


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
        serializer = TicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data.get('file')
        if isinstance(file, InMemoryUploadedFile):
            file = convert_to_temporary_uploaded_file(file)

        if '.pdf' in file.name:
            station_recognition_service = PDFStationRecognitionService(file)
        elif has_image_extension(file.name):
            station_recognition_service = ImageStationRecognitionService(file)
        else:
            raise ValidationError(detail=f'File format is not supported. Use {", ".join(IMAGE_EXTENTSIONS)} or .pdf.', code=HTTP_400_BAD_REQUEST)

        result = station_recognition_service.recognite()

        distance = 0
        for data in result:
            origin = data.get('origin').lower()
            destination = data.get('destination').lower()

            ticket_distance = CalculateDistanceService().calculate_distance(origin, destination)
            distance += ticket_distance
            user = request.user

            station_recognition_service.save_ticket(origin, destination, data.get('ticket_number'), user)
            user.update_distance(ticket_distance)

        return Response(data={'distance': distance})
