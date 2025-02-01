"""Admnin.py
"""

from django.contrib import admin

from .models import Booking, Payment, Room

admin.site.register(Booking)
admin.site.register(Room)
admin.site.register(Payment)
