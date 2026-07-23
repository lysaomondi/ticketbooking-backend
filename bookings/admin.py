from django.contrib import admin
from .models import Venue, Event, TicketType, Booking, Payment

admin.site.register(Venue)
admin.site.register(Event)
admin.site.register(TicketType)
admin.site.register(Booking)
admin.site.register(Payment)