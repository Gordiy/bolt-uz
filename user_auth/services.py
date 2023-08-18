"""Services for user_auth app."""
from user_auth.models import BoltUser


class BoltUserService:
    """User service."""
    @staticmethod
    def update_user_distance(user: BoltUser, distance: int) -> None:
        """
        After recieving coupon update user distance.
        
        :param user: user instance.
        :param distance: coupon distance.
        :return: None.
        """
        user.distance = user.distance - distance
        user.save()
