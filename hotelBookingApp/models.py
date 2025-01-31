"""This module contains the models for the hotel booking application."""

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


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
    room_number = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        help_text="The number of the room."
    )
    room_type = models.CharField(
        max_length=20,
        choices=ROOM_TYPES,
        help_text="The type of the room (e.g., single, double, suite)."
    )
    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="The price per night for the room."
    )

    def __str__(self):
        """Returns a string representation of the Room object.
        """
        return (
            f"{self.room_type} - Room number - {self.room_number}"
        )

    def save(self, *args, **kwargs):
        """
        Automatically set the room_number to the id of the room after saving.
        """
        if not self.room_number and not self.id: #pylint: disable=no-member
            # First save to get an ID
            super().save(*args, **kwargs)
            # Set the room number
            self.room_number = str(self.id) # pylint: disable=no-member
            # Save again to update the room_number
            super().save(*args, **kwargs)
        else:
            # Normal save for updates
            super().save(*args, **kwargs)

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
    check_in_date = models.DateField(default=now)
    check_out_date = models.DateField(default=now)
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
        # Prevent double booking of the same room for the same dates
        unique_together = ('room', 'check_in_date', 'check_out_date')
        ordering = ['check_in_date']

    def __str__(self):
        """Returns a string representation of the Booking object.
        """
        return (
            f"""Room type {self.room.room_type} number {self.room.room_number}
            booked by {self.user.username} from {self.check_in_date} to {self.check_out_date}""" # pylint: disable=no-member
        )
