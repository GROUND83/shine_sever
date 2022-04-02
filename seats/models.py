from django.db import models
from cores import models as core_models


class RoomType(core_models.TimeStampedModel):
    name = models.CharField(max_length=80)

    class Meta:

        verbose_name = "열람실명"
        verbose_name_plural = "열람실 모음"

    def __str__(self):

        return self.name


class SeatType(core_models.TimeStampedModel):
    name = models.CharField(max_length=80)

    class Meta:

        verbose_name = "좌석타입"
        verbose_name_plural = "좌석타입 모음"

    def __str__(self):

        return self.name


class Seat(core_models.TimeStampedModel):
    class Meta:
        verbose_name = "좌석"
        verbose_name_plural = "좌석 모음"

    name = models.CharField(max_length=50, null=True, verbose_name="좌석이름")
    seat_type = models.ForeignKey(
        SeatType, on_delete=models.SET_NULL, null=True, verbose_name="좌석타입"
    )
    room_type = models.ForeignKey(
        RoomType, on_delete=models.SET_NULL, null=True, verbose_name="열람실"
    )
    lightId = models.CharField(max_length=50, null=True, verbose_name="조명 id")
    is_light_on = models.BooleanField(
        max_length=50, default=False, verbose_name="조명 상태"
    )
    is_seat_full = models.BooleanField(
        max_length=50, default=False, verbose_name="좌석 상태"
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="회원",
    )

    def __str__(self):
        return f"{self.room_type}{self.seat_type}{self.name}"
