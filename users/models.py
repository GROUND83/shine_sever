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

    USER_TYPE = (
        ("관리자", "관리자"),
        ("일반", "일반"),
        ("학생", "학생"),
    )
    GENDER_TYPE = (
        ("남", "남"),
        ("여", "여"),
    )
    gender = models.CharField(
        max_length=50, choices=GENDER_TYPE, null=True, verbose_name="성별"
    )
    phone = models.CharField(
        max_length=50, unique=True, null=True, blank=True, verbose_name="전화번호"
    )
    user_birth = models.DateField(
        max_length=50, null=True, blank=True, verbose_name="생년월일"
    )
    user_type = models.CharField(
        max_length=50, choices=USER_TYPE, null=True, verbose_name="회원타입"
    )
    username = models.CharField(max_length=50, unique=False, verbose_name="이름")

    personalPolicy = models.BooleanField(default=False, verbose_name="개인정보호정책/이용약관")

    school_name = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="학교이름"
    )
    school_grade = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="학년"
    )

    onsignalId = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="푸쉬아이디"
    )
    deviceId = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="디바이스아이디"
    )
    qrauthcode = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="qrauthcode"
    )
    qrtime = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="qrtime"
    )
    timeAlram = models.BooleanField(default=True, verbose_name="시간대알림")
    eventAlram = models.BooleanField(default=True, verbose_name="이벤트알림")
    user_image = models.ImageField(
        upload_to="users/",
        null=True,
        blank=True,
    )
    is_black = models.BooleanField(
        default=False, null=True, blank=True, verbose_name="블랙"
    )

    objects = core_managers.CustomUserManager()

    USERNAME_FIELD = "phone"

    def __str__(self):
        return self.username
