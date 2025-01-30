"""Module for views for each serializer
ViewSets automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions.
"""

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from .models import Room, Booking
from .serializers import BookingSerializer, RoomSerializer

class RoomViewSet(viewsets.ModelViewSet):
    """A simple viewSet for viewing rooms
    """
    queryset = Room.objects.all() # pylint: disable=no-member
    serializer_class = RoomSerializer
    permission_classes = [permissions.AllowAny] # All users can view rooms

    @action(detail=False, methods=['get'], url_path='available')
    def available_rooms(self, request):
        """Custom endpoint to filter available rooms based on check-in and check-out dates.

        Returns:
            list:Available rooms for the given dates and room type.
        """
        check_in_date = request.query_params.get('check_in_date')
        check_out_date = request.query_params.get('check_out_date')
        room_type = request.query_params.get('room_type', None)

        if not check_in_date or not check_out_date:
            return Response(
                {"error": "Please provide both check_in_date and check_out_date dates."},
                status=400
            )

        # Filter rooms NOT booked for the given date range using Booking Model
        booked_rooms = Booking.objects.filter( # pylint: disable=no-member
            Q(check_in_date__lte=check_out_date) & Q(check_out_date__gte=check_in_date)
        ).values_list('room_id', flat=True)

        # exclude these booked rooms from the list of all rooms
        available_rooms = Room.objects.exclude(id__in=booked_rooms) # pylint: disable=no-member

        # If room_type is provided, filter by room type
        if room_type:
            available_rooms = available_rooms.filter(room_type=room_type)

        serializer = self.get_serializer(available_rooms, many=True)
        return Response(serializer.data)


