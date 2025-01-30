"""This module contains the models for the hotel booking application."""

from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    """Represents a room in the hotel

    Attributes:
        room_type (str): The type of the room (e.g., single, double, suite).
        price_per_night (Decimal): The price per night for the room.
        total_rooms (int): The total number of rooms of this type in the
        hotel.
        available_rooms (int): The number of rooms of this type currently
        available for booking.

    Returns:
        __str__(): Returns a string representation of the room, including
        its type and availability.
    """
    ROOM_TYPES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
    ]
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    total_rooms = models.IntegerField()
    available_rooms = models.IntegerField()

    def __str__(self):
        """Returns a string representation of the Room object.
        """
        return (
            f"{self.room_type} - {self.total_rooms} total rooms - {self.available_rooms} available"
        )

class Booking(models.Model):
    """Represents a booking made by a user for a specific room.

    Attributes:
        user (User): The user who made the booking.
        room (Room): The room that was booked.
        check_in_date (date): The check-in date for the booking.
        check_out_date (date): The check-out date for the booking.
        created_at (datetime): The timestamp when the booking was created.

    Returns:
       __str__(): Returns a string representation of the booking, including
       the username and room type.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Metadata for the Booking model.

        Constraints:
            unique_together: Ensures that a user cannot book the same room
            for the same check-in date more than once.

        Options:
            ordering: Default ordering for Booking objects is by the
            'check_in_date' in ascending order.
        """
        unique_together = ('user', 'room', 'check_in_date')
        ordering = ['check_in_date']

    def __str__(self):
        """Returns a string representation of the Booking object.
        """
        return f"Room type {self.room.room_type} booked by {self.user}"
