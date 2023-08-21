"""Enums for coupons app."""
from enum import Enum

from coupons.constants import DISTANCE_INDEX, PRICE_AND_DISTANCE


class CouponsErrors(Enum):
    """Enum describes error messages for coupons viewset."""
    TOO_SMALL_DISTANCE = f'Your distance less than {PRICE_AND_DISTANCE[0][DISTANCE_INDEX]}.'
    NO_COUPONS_AVAILIABLE = 'No coupons available'


class StationRecognitionErrors(Enum):
    """Enum describes error messages for station recognition service."""
    EMPTY_IMAGE = 'The image is empty.'
    DEPARTMENT_OR_APPOINTMENT_NOT_FOUD = 'The image does not contain departure or appointment.'
    TICKET_ALREADY_USED = 'Ticket already used.'
