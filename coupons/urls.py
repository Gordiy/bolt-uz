from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CouponViewSet, TicketViewSet

router = DefaultRouter()
router.register(r'coupons', CouponViewSet)
router.register(r'tickets', TicketViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
