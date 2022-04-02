from django.contrib.auth.models import AbstractUser
from django.db import models
from cores import managers as core_managers
from cores import models as core_models


class UserType(core_models.TimeStampedModel):
    name = models.CharField(max_length=80)

    class Meta:
        verbose_name = "회원타입"
        verbose_name_plural = "회원타입 모음"

    def __str__(self):

        return self.name


class User(AbstractUser):
    class Meta:
        verbose_name_plural = "고객"

    phone = models.CharField(
        max_length=50, unique=True, null=True, blank=True, verbose_name="전화번호"
    )
    user_birth = models.DateField(
        max_length=50, null=True, blank=True, verbose_name="생년월일"
    )
    user_type = models.ForeignKey(
        UserType, on_delete=models.SET_NULL, null=True, verbose_name="회원타입"
    )
    username = models.CharField(max_length=50, unique=False, verbose_name="이름")

    personalPolicy = models.BooleanField(default=False, verbose_name="개인정보호정책/이용약관")
    # servicePolicy = models.BooleanField(default=False, verbose_name="이용약관")
    parent_phone = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="부모전화번호"
    )
    parent_name = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="부모성함"
    )
    is_shine = models.BooleanField(
        default=False, null=True, blank=True, verbose_name="샤인학원학생"
    )

    school_name = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="학교이름"
    )
    school_grade = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="학년"
    )

    onsignalId = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="푸쉬아이디"
    )

    timeAlram = models.BooleanField(default=True, verbose_name="시간대알림")
    eventAlram = models.BooleanField(default=True, verbose_name="이벤트알림")
    user_image = models.ImageField(
        upload_to="images/",
        null=True,
        blank=True,
    )
    is_black = models.BooleanField(
        default=False, null=True, blank=True, verbose_name="블랙"
    )
    objects = core_managers.CustomUserManager()

    USERNAME_FIELD = "phone"

    def __str__(self):
        return self.phone
