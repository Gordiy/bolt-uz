"""Views for coupons app."""
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import DestroyModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet

from .constants import IMAGE_EXTENTSIONS
from .models import Coupon, Ticket
from .serializers import (CouponSerializer, TicketSerializer,
                          TickeUploadFiletSerializer)
from .services import (CalculateDistanceService, CouponService,
                       PDFStationRecognitionService)
from .tasks import image_station_recognition
from .utils import (convert_to_temporary_uploaded_file,
                    deepcopy_temporary_uploaded_file, has_image_extension)
from django.db.utils import IntegrityError


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


class TicketViewSet(RetrieveModelMixin, GenericViewSet):
    """Viewset to upload ticket."""
    queryset = Ticket.objects.all()
    permission_classes = [IsAuthenticated | IsAdminUser]
    serializer_class = TicketSerializer

    @action(detail=False, methods=['POST'])
    def upload_ticket(self, request: HttpRequest) -> HttpResponse:
        """
        Upload ticket.
        
        :param request: http request.
        :return: http response.
        """
        serializer = TickeUploadFiletSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user

        file = serializer.validated_data.get('file')
        if isinstance(file, InMemoryUploadedFile):
            file = convert_to_temporary_uploaded_file(file)

        if '.pdf' in file.name:
            station_recognition_service = PDFStationRecognitionService(file)
        elif has_image_extension(file.name):
            try:
                ticket = Ticket.objects.create(file=file, unique_number=file.name, user=user)
            except IntegrityError:
                raise ValidationError(detail="Ticket already uploaded.", code=HTTP_400_BAD_REQUEST)
            image_station_recognition.apply_async(kwargs={"ticket_id": ticket.id})

            return Response(data={'id': ticket.id})
        else:
            raise ValidationError(detail=f'File format is not supported. Use {", ".join(IMAGE_EXTENTSIONS)} or .pdf.', code=HTTP_400_BAD_REQUEST)

        result = station_recognition_service.recognite()

        distance = 0
        for data in result:
            origin = data.get('origin').lower()
            destination = data.get('destination').lower()

            ticket_distance = CalculateDistanceService().calculate_distance(origin, destination)
            distance += ticket_distance

            station_recognition_service.file = deepcopy_temporary_uploaded_file(file)
            station_recognition_service.save_ticket(origin, destination, data.get('ticket_number'), user)
            user.update_distance(ticket_distance)

        return Response(data={'distance': distance})
