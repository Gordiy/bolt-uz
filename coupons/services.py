"""Services for coupons app."""
from django.db.models.query import QuerySet
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_400_BAD_REQUEST

from coupons.constants import DISTANCE_INDEX, PRICE_AND_DISTANCE
from coupons.enums import CouponsErrors
from coupons.models import Coupon
from user_auth.models import BoltUser


class CouponService:
    """The service describes methods of working with the Coupon instance."""
    def get_coupon_by_distance(self, user: BoltUser) -> Coupon or ValidationError:
        """
        Get coupon by distance and assign it to user.
        
        :param user: user.
        :raises ValidationError: if any coupons do not exists.
        :return: coupon.
        """
        coupons = Coupon.objects.filter(user__isnull=True)
        self._check_distance(user.distance)
        coupon = self._get_coupon_by_distance(user.distance, coupons)

        if not coupon:
            raise ValidationError(detail=CouponsErrors.NO_COUPONS_AVAILIABLE.value, code=HTTP_400_BAD_REQUEST)

        coupon.user = user
        coupon.save()

        return coupon
        
    @staticmethod        
    def _check_distance(distance: int) -> None or ValidationError:
        """
        Check if the user's distance is enough to get the coupon.
        
        :param distance: user distance.
        :raises ValidationEror: if user distance to small.
        :return: None.
        """
        if distance < PRICE_AND_DISTANCE[0][DISTANCE_INDEX]:
            raise ValidationError(detail=CouponsErrors.TOO_SMALL_DISTANCE.value, code=HTTP_400_BAD_REQUEST)

    @staticmethod
    def _get_coupon_by_distance(distance: int, coupons: QuerySet[Coupon]) -> Coupon or None:
        """
        Get coupon by distance.
        
        :param distance: user distance.
        :param coupons: list of availiable coupons.
        :return: coupon if found else None.
        """
        if distance >= PRICE_AND_DISTANCE[0][DISTANCE_INDEX] and distance <= PRICE_AND_DISTANCE[1][DISTANCE_INDEX]:
            return coupons.filter(distance=PRICE_AND_DISTANCE[0][DISTANCE_INDEX]).first()
        elif distance >= PRICE_AND_DISTANCE[1][DISTANCE_INDEX] and distance <= PRICE_AND_DISTANCE[2][DISTANCE_INDEX]:
            return coupons.filter(distance=PRICE_AND_DISTANCE[1][DISTANCE_INDEX]).first()
        elif distance >= PRICE_AND_DISTANCE[2][DISTANCE_INDEX] and distance <= PRICE_AND_DISTANCE[3][DISTANCE_INDEX]:
            return coupons.filter(distance=PRICE_AND_DISTANCE[2][DISTANCE_INDEX]).first()
        elif distance >= PRICE_AND_DISTANCE[3][DISTANCE_INDEX]:
            return coupons.filter(distance=PRICE_AND_DISTANCE[3][DISTANCE_INDEX]).first()
