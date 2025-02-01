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
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField(default=now)
    check_out_date = models.DateField(default=now)
    total_booking_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=10,
        choices = PAYMENT_STATUS,
        default='pending'
    )

    class Meta:
        """Metadata for the Booking model.
        """
        ordering = ['-created_at'] # Make the latest booking appear first in records

    def save(self, *args, **kwargs):
        """
        Override the save method to calculate the total_booking_price before saving.
        """
        if self.check_in_date and self.check_out_date and self.room:
            num_nights = (self.check_out_date - self.check_in_date).days
            if num_nights == 0:
                num_nights = 1
            self.total_booking_price = num_nights * self.room.price_per_night # pylint: disable=no-member
        super().save(*args, **kwargs)

    def __str__(self):
        """Returns a string representation of the Booking object.
        """
        return (
            f"""Room type {self.room.room_type} number {self.room.room_number}
            booked by {self.user.username} from {self.check_in_date} to {self.check_out_date}""" # pylint: disable=no-member
        )


class Payment(models.Model):
    """Represents a payment made for a specific booking.

    This model stores the payment details for a booking, including the card information
    (masked for security), the payment amount, and the timestamp when the payment was created.

    Attributes:
        booking: Each booking can have only one payment.
        card_number (CharField): The card number used for the payment.
        card_expiry (CharField): The expiry date of the card in the format MM/YY.
        cvv (CharField): The CVV (Card Verification Value) of the card.
        amount (DecimalField): The total amount paid for the booking.
        created_at (DateTimeField): The timestamp when the payment was created.

    Returns:
        str: A string representation of the payment.
    """
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    card_number = models.CharField(max_length=20, help_text="Enter card number")
    card_expiry = models.CharField(max_length=5, help_text=" Format: MM, YY")
    card_cvv = models.CharField(max_length=3, help_text=" Format: 3 digits")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        """
        Override the save method to strip the extra characters from card number.
        """
        self.card_number = self.card_number.strip()  # Remove any extra spaces or newlines
        super().save(*args, **kwargs)


    def __str__(self):
        """Returns a string representation of the Payment object.
        """
        return f"Payment for Booking {self.booking.id} - Amount: {self.amount}" # pylint: disable=no-member
