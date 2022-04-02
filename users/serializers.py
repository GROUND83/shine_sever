from rest_framework import serializers
from .models import User

# from alrams.serializers import AlramSerializer
# from orders.serializers import OrderSerializer

# 회원가입 시리얼라이저


# 접속 유지중인지 확인할 시리얼라이저
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # alrams = AlramSerializer(many=True)
    # orders = OrderSerializer(many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "phone",
            "username",
            "password",
            "timeAlram",
            "eventAlram",
            "personalPolicy",
            "is_staff",
        )
        read_only_fields = ("id",)


class UserTinySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name")
