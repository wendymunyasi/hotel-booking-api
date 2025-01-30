"""Module for permissions
"""

from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Custom permission to allow only the owner of a booking to view it.
    """
    def has_object_permission(self, request, view, obj):
        """Check if the booking belongs to the logged-in user

        Returns:
            obj: user
        """
        return obj.user == request.user
