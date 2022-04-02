from django.db import models
from cores import models as core_models


class Vertifie(core_models.TimeStampedModel):
    phone = models.CharField(max_length=11, null=True, verbose_name="phone")
    code = models.CharField(max_length=4, null=True, verbose_name="code")

    def __str__(self):
        return f"{self.phone}"
