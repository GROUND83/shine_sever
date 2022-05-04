from django.db import models
from cores import models as core_models
import datetime


class Seat(core_models.TimeStampedModel):
    class Meta:
        verbose_name = "좌석"
        verbose_name_plural = "좌석 모음"

    SEAT_TYPE = (
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("S", "S"),
    )
    ROOM_TYPE = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
    )

    name = models.CharField(max_length=50, null=True, verbose_name="좌석번호")
    seat_type = models.CharField(
        max_length=50, choices=SEAT_TYPE, null=True, verbose_name="좌석타입"
    )
    room_type = models.CharField(
        max_length=50, choices=ROOM_TYPE, null=True, verbose_name="열람실"
    )

    seat_title = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="좌석타이틀"
    )
    lightId = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="조명 id",
    )
    is_light_on = models.BooleanField(
        max_length=50, default=False, null=True, blank=True, verbose_name="조명 상태"
    )
    is_seat_full = models.BooleanField(
        max_length=50, default=False, null=True, blank=True, verbose_name="좌석 상태"
    )
    is_reservation = models.BooleanField(
        max_length=50, default=False, null=True, blank=True, verbose_name="예약"
    )
    end_date = models.DateField(
        auto_now=False, null=True, blank=True, verbose_name="종료일"
    )
    is_clean = models.BooleanField(
        max_length=50, default=False, null=True, blank=True, verbose_name="짐상태"
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default="",
        related_name="회원",
    )

    def __str__(self):
        return self.seat_title

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         super().save(*args, **kwargs)
    #     # self.seat_title = self.room_type + self.seat_type + self.name
    #     super(Seat, self).save(*args, **kwargs)
