from rest_framework import serializers
from .models import Seat

from rest_framework.response import Response
from rest_framework import status

import datetime
from random import randint

from users.serializers import UserSerializer

import json


class SeatSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Seat

        fields = [
            "id",
            "name",
            "seat_type",
            "room_type",
            "seat_title",
            "lightId",
            "is_light_on",
            "is_seat_full",
            "is_reservation",
            "end_date",
            "is_clean",
            "owner",
        ]
