from rest_framework import serializers
from .models import Check
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserSerializer


class CheckSerializer(serializers.ModelSerializer):
    seatUser = UserSerializer()

    class Meta:
        model = Check

        fields = [
            "seatName",
            "seatUser",
            "check_type",
            "created",
        ]
