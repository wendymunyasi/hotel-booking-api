"""Module for views for each serializer
"""

from django.shortcuts import render
from rest_framework import viewsets
from .models import Room, Booking
from .serializers import BookingSerializer, RoomSerializer

class RoomViewSet(viewsets.ModelViewSet):
    """A simple viewSet for viewing rooms
    """
    queryset = Room.objects.all() # pylint: disable=no-member
    serializer_class = RoomSerializer

class BoookingViewSet(viewsets.ModelViewSet):
    """A simple viewSet for viewing Bookings
    """
    queryset = Booking.objects.all() # pylint: disable=no-member
    serializer_class = BookingSerializer
