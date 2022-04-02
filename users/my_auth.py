from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from .models import User


class UserBackend(ModelBackend):
    def authenticate(self, request):
        phone = request.data.get("phone")
        user = User.objects.get(phone=phone)
        if user:
            return user

        else:
            return None
            # phone = request.data.get("phone")
            # firstName = request.data.get("firstName")

            # user = User.objects.create(
            #     username=email, email=email, first_name=firstName, phone=phone,
            # )

            # user.save()
            # return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
