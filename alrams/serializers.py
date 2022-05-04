from rest_framework import serializers
from .models import Alram
from users.serializers import UserSerializer


class AlramSerializer(serializers.ModelSerializer):
    to = UserSerializer()

    class Meta:
        model = Alram
        fields = ["id", "headings", "subtitle", "senttime", "to", "created","updated"]
