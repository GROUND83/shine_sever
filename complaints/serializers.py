from rest_framework import serializers
from .models import Complaint
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserSerializer

class CompliantSerializer(serializers.ModelSerializer):
  author = UserSerializer()

  class Meta:
      model = Complaint

      fields = [
          "id",
          "content",
          "complaintype",
          "author",
          "answer",
          "created"
      ]
