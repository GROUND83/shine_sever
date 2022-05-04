from django.contrib import admin
from . import models
from ewelink.ewelink import Ewelink
from .models import Seat
import os
from pathlib import Path
import json
from django.core.exceptions import ImproperlyConfigured
# Register your models here.
@admin.register(models.Seat)
class SeatAdmin(admin.ModelAdmin):
 
    list_display = [
        "seat_title",
        "room_type",
        "seat_type",
        "name",
        "lightId",
        "is_light_on",
        "is_seat_full",
        "is_reservation",
        "end_date",
        "owner",
        "is_clean",
    ]

    # list_display_links = [
    #     "menu",
    # ]
    search_fields = ("=seat_seat_title",)
