"""Module for views for each serializer
ViewSets automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions.
"""

from django.db.models import Q
from rest_framework import permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking, Payment, Room
from .permissions import IsOwner
from .serializers import (BookingSerializer, PaymentSerializer, RoomSerializer,
                          UserRegistrationSerializer)


class RoomViewSet(viewsets.ModelViewSet):
    """A simple viewSet for viewing rooms
    """
    queryset = Room.objects.all() # pylint: disable=no-member
    serializer_class = RoomSerializer
    permission_classes = [permissions.AllowAny] # All users can view rooms
    # http_method_names = ['get'] # Only allow get requests

    @action(detail=False, methods=['get'], url_path='available')
    def available_rooms(self, request):
        """Custom endpoint to filter available rooms based on check-in and check-out dates.
        Users can be able to filter by room type as well.

        Query Parameters:
            - room_type (Optional): The type of room (e.g., single, double, suite).
            - check_in_date: The check-in date to filter available rooms.
            - check_out_date: The check-out date to filter available rooms.

        Returns:
            list:Available rooms for the given dates and room type.
        """
        check_in_date = request.query_params.get('check_in_date')
        check_out_date = request.query_params.get('check_out_date')
        room_type = request.query_params.get('room_type', None)

        if not check_in_date or not check_out_date:
            return Response(
        {
            "error": (
                "Please provide both check_in_date and check_out_date. You can also "
                "provide room_type if you want to filter by room type."
            )
        },
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

        # Serialize the available rooms
        serializer = self.get_serializer(available_rooms, many=True)
        data = serializer.data

        # Group rooms by room_type using a dictionary
        grouped_data = {}
        for room in data:
            room_type = room["room_type"]
            if room_type not in grouped_data:
                grouped_data[room_type] = []
            grouped_data[room_type].append(room)

        # Return the grouped data
        return Response(grouped_data)


    def create(self, request, *args, **kwargs):
        """Override the create method to customize the response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer) # Call the serializer create method
        headers = self.get_success_headers(serializer.data)

        # Customize the response data
        response_data = {
            "message": "Room created successfully. Well done, champ!",
            "data": serializer.data
        }

        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class BoookingViewSet(viewsets.ModelViewSet):
    """A simple viewSet for viewing Bookings
    """
    queryset = Booking.objects.all() # pylint: disable=no-member
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner] # Only logged-in users can book
    # permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post','delete'] # Only allow these requests

    def perform_create(self, serializer):
        """Create a new booking and associate it with the logged-in user
        """
        # Automatically associate the booking with the logged-in user
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """View all bookings for the logged-in user
        """
        # Allow users to view only their own bookings
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Override the create method to return a custom success message
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "data": serializer.data,
                "message": "Booking created successfully."
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def destroy(self, request, *args, **kwargs):
        """Override the destroy method to return a custom success message
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Booking deleted successfully."},
            status=status.HTTP_200_OK
        )

# Login View
class LoginView(ObtainAuthToken):
    """
    View to handle user login and return an authentication token.
    """
    def post(self, request, *args, **kwargs):
        """Generate and return an authentication token for the user
        """
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token']) # pylint: disable=no-member
        return Response(
            {
                'data': {
                    'token': token.key,
                    'user_id': token.user_id,
                    'username': token.user.username,
                },
                'message': 'Login successful'
            }
        )

# Logout View
class LogoutView(APIView):
    """
    View to handle user logout by deleting their authentication token.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Delete the user's authentication token
        """
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully."})

class UserRegistrationView(APIView):
    """
    View to handle user registration.
    """
    def post(self, request):
        """Register a user
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user =  serializer.save()
            # Generate a token for the user
            token = Token.objects.create(user=user) # pylint: disable=no-member
            return Response({
                "message": "User registered successfully.",
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentViewSet(viewsets.ModelViewSet):
    """A simple viewSet for viewing Payments
    """
    queryset = Payment.objects.all() # pylint: disable=no-member
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Create a payment for a specific booking.
        """
        booking_id = kwargs.get('booking_id')
        try:
            # Retrieve the booking object and user
            booking = Booking.objects.get(id=booking_id, user=request.user) # pylint: disable=no-member
        except Booking.DoesNotExist: # pylint: disable=no-member
            return Response(
                {"error": "Booking not found or not authorized."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if the payment is already completed
        if booking.payment_status == 'completed':
            return Response(
                {"error": "Payment already completed for this booking."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate the payment data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Inject the booking and amount into the validated data
        validated_data = serializer.validated_data
        validated_data['booking'] = booking
        validated_data['amount'] = booking.room.price_per_night  # Get the price from the room

        # Dummy payment processing logic
        payment_successful = True  # Simulate payment success
        if payment_successful:
            serializer.save(booking=booking, amount=booking.room.price_per_night)
            booking.payment_status = 'completed'
            booking.save()
            return Response(
                {
                "data": serializer.data,
                "message": "Payment completed successfully."
                },
                status=status.HTTP_201_CREATED
            )
        else:
            booking.payment_status = 'failed'
            booking.save()
            return Response({"error": "Payment failed."}, status=status.HTTP_400_BAD_REQUEST)
