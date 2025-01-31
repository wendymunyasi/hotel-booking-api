"""Module for serializing the models so that they can be exposed to the API.
"""

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Booking, Room

# Serializers allow complex data such as querysets and model instances to
# be converted to native Python datatypes that can then be easily rendered
# into JSON, XML or other content types. Serializers also provide
# deserialization, allowing parsed data to be converted back into complex
# types, after first validating the incoming data.

class RoomSerializer(serializers.ModelSerializer):
    """Serialzier to map the Room model to the JSON format
    Represents the Room model in API responses
    """

    class Meta:
        """Meta class to define the model and fields to include in the serializer.
        """
        model = Room
        fields = ['room_number', 'room_type', 'price_per_night']

class BookingSerializer(serializers.ModelSerializer):
    """
    Serialzier to map the Booking model to the JSON format
    Represents the Booking model in API responses
    """

    room = RoomSerializer(read_only=True)
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(), source='room', write_only=True # pylint: disable=no-member
    )

    class Meta:
        """Meta class to define the model and fields to include in the serializer.
        """
        model = Booking
        fields = ['id', 'room', 'room_id', 'check_in_date', 'check_out_date']
        read_only_fields = ['user']

    def validate(self, data): # pylint: disable=arguments-renamed
        """
        Validate the booking data to ensure check-in is before check-out
        and that the room is not already booked for the selected dates.
        """
        # Ensure check-in is before check-out
        if data['check_in_date'] >= data['check_out_date']:
            raise serializers.ValidationError("Check-in date must be before check-out date.")

        # Check if the room is already booked for the given dates
        overlapping_bookings = Booking.objects.filter( # pylint: disable=no-member
            room=data['room'],
            check_in_date__lt=data['check_out_date'],
            check_out_date__gt=data['check_in_date']
        )
        if overlapping_bookings.exists():
            raise serializers.ValidationError("The room is already booked for the selected dates.")

        return data

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serialzier to map the User model to the JSON format
    Represents the User model in API responses
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        """Meta class to define the model and fields to include in the serializer.
        """
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def validate(self, data): # pylint: disable=arguments-renamed
        """Check if passwords match
        """
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        """Create a new user
        """
        # Remove password_confirm from validated_data
        validated_data.pop('password_confirm')
        # Create the user
        user = User.objects.create_user(**validated_data)
        return user
