from rest_framework import viewsets, permissions
from .models import Venue, Event, TicketType
from .serializers import VenueSerializer, EventSerializer, TicketTypeSerializer
from .permissions import IsOrganizer, IsOwnerOrAdmin
from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Booking, TicketType, Payment
from .serializers import BookingCreateSerializer, BookingSerializer
from .models import Payment
from .serializers import PaymentSerializer


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            return [IsOrganizer()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsOrganizer(), IsOwnerOrAdmin()]
        return [permissions.AllowAny()]  # anyone can browse/view events

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


class TicketTypeViewSet(viewsets.ModelViewSet):
    queryset = TicketType.objects.all()
    serializer_class = TicketTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CreateBookingView(generics.CreateAPIView):
    serializer_class = BookingCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ticket_type_id = serializer.validated_data["ticket_type"].id
        quantity = serializer.validated_data["quantity"]

        with transaction.atomic():
        
            ticket_type = TicketType.objects.select_for_update().get(id=ticket_type_id)

            remaining = ticket_type.quantity_available - ticket_type.quantity_sold
            if quantity > remaining:
                return Response(
                    {"detail": f"Only {remaining} tickets left."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            ticket_type.quantity_sold += quantity
            ticket_type.save()

            booking = Booking.objects.create(
                user=request.user,
                ticket_type=ticket_type,
                quantity=quantity,
                total_price=ticket_type.price * quantity,
                status="pending",
            )

        output = BookingSerializer(booking)
        return Response(output.data, status=status.HTTP_201_CREATED)


class MyBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
    
class CreatePaymentView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        booking_id = request.data.get("booking")
        booking = Booking.objects.get(id=booking_id, user=request.user)

        # Simulated payment - in real life this is where you'd call M-Pesa/Stripe
        payment = Payment.objects.create(
            booking=booking,
            amount=booking.total_price,
            method=request.data.get("method", "mock"),
            status="success",
            transaction_reference=f"MOCK-{booking.id}-{booking.user.id}",
        )

        booking.status = "confirmed"
        booking.save()

        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)