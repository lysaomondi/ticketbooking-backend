from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    VenueViewSet, EventViewSet, TicketTypeViewSet,
    CreateBookingView, MyBookingsView, CreatePaymentView,
)

router = DefaultRouter()
router.register("venues", VenueViewSet)
router.register("events", EventViewSet)
router.register("ticket-types", TicketTypeViewSet)

urlpatterns = router.urls + [
    path("bookings/", CreateBookingView.as_view(), name="create-booking"),
    path("bookings/mine/", MyBookingsView.as_view(), name="my-bookings"),
    path("payments/", CreatePaymentView.as_view(), name="create-payment"),
]