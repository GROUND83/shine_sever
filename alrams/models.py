from django.db import models
from cores import models as core_models
import datetime


class Alram(core_models.TimeStampedModel):
    class Meta:
        verbose_name = "알림"
        verbose_name_plural = "알림 모음"
        ordering = ["-created"]

    headings = models.CharField(max_length=200, null=True, verbose_name="타이틀")
    subtitle = models.CharField(max_length=200, null=True, verbose_name="서브타이틀")
    contents = models.TextField(null=True, verbose_name="설명")
    sented = models.BooleanField(default=False, verbose_name="발송")
    senttime = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name="발송시간"
    )
    to = models.ForeignKey(
        "users.user",
        on_delete=models.SET_NULL,
        null=True,
        related_name="유져",
        verbose_name="대상자",
    )

    def __str__(self):
        return self.headings
