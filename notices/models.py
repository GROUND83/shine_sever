from django.db import models
from cores import models as core_models
import datetime


class Notice(core_models.TimeStampedModel):
    class Meta:
        verbose_name = "공지사항"
        verbose_name_plural = "공지사항 모음"
        ordering = ["-created"]

    title = models.CharField(max_length=200, null=True, verbose_name="타이틀")
    subTitle = models.TextField(null=True, verbose_name="설명")

    def __str__(self):
        return self.title
