from django.db import models
from cores import models as core_models
# Create your models here.



class Check(core_models.TimeStampedModel):
  class Meta:
        verbose_name = "입실기록"
        verbose_name_plural = "입실기록 모음"

  CHECK_TYPE = (
        ("입실", "입실"),
        ("퇴실", "퇴실"),
   
    
    )
  seatName = models.CharField(max_length=50, null=True, verbose_name="좌석번호")
  seatUser = models.ForeignKey("users.user",on_delete=models.SET_NULL,null=True, verbose_name="입실회원")
  check_type = models.CharField(
        max_length=50, choices=CHECK_TYPE, null=True, verbose_name="입실타입"
    )
