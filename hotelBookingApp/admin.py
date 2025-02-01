"""Admnin.py
"""

from django.contrib import admin

from .models import Booking, Room, Payment

admin.site.register(Booking)
admin.site.register(Room)
admin.site.register(Payment)
