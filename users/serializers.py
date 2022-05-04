from rest_framework import serializers
from .models import User

# from alrams.serializers import AlramSerializer
# from orders.serializers import OrderSerializer

# 회원가입 시리얼라이저


# 접속 유지중인지 확인할 시리얼라이저
class UserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)

    # orders = OrderSerializer(many=True)
    user_image = serializers.ImageField(
        max_length=None, use_url=True, allow_null=True, required=False
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "phone",
            "user_type",
            "user_birth",
            "gender",
            "school_name",
            "school_grade",
            "timeAlram",
            "eventAlram",
            "personalPolicy",
            "user_image",
            "deviceId",
            "onsignalId",
        ]

        read_only_fields = ("id",)
