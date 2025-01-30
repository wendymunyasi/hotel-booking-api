"""Module for serializing the models so that they can be exposed to the API.
"""

from rest_framework import serializers
from .models import Room, Booking

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
        fields = ['id', 'room_type', 'price_per_night', 'available_rooms', 'total_price']

class BookingSerializer(serializers.ModelSerializer):
    """
    Serialzier to map the Booking model to the JSON format
    Represents the Booking model in API responses
    """
    class Meta:
        """Meta class to define the model and fields to include in the serializer.
        """
        model = Booking
        fields = ['id', 'user', 'room', 'check_in_date', 'check_out_date',
                    'name', 'contact', 'email', 'created_at']
