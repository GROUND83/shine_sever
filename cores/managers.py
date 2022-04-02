from django.db import models
from django.contrib.auth.models import UserManager


class CustomModelManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None

    def create_superuser(
        self,
        username="관리자",
        **extra_fields,
    ):

        user = self.create_user(username, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUserManager(CustomModelManager, UserManager):
    pass
