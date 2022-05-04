from rest_framework import serializers
from .models import Order

from rest_framework.response import Response
from rest_framework import status

import datetime
from random import randint
from users.models import User
from users.serializers import UserSerializer
from seats.serializers import SeatSerializer

import json


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    seat = SeatSerializer(read_only=True)

    class Meta:
        model = Order
        read_only_fields = (
            "id",
            "created",
        )
