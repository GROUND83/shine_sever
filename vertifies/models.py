from django.db import models
from cores import models as core_models

# sms인증코드
class Vertifie(core_models.TimeStampedModel):
    phone = models.CharField(max_length=11, null=True, verbose_name="phone")
    code = models.CharField(max_length=4, null=True, verbose_name="code")

    limitTime  = models.DateTimeField(auto_now=False,null=True, verbose_name="제한시간")
    def __str__(self):
        return f"{self.phone}"
