
from django.db import models
from cores import models as core_models



class Complaint(core_models.TimeStampedModel):
  class Meta:
        verbose_name = "컴플레인"
        verbose_name_plural = "컴플레인 모음"

  CHECK_TYPE = (
      ("요청", "요청"),
      ("답변", "답변"),
  
  )
  content  = models.TextField(null=True, verbose_name="내용")
  complaintype = models.CharField(max_length=50, choices=CHECK_TYPE, null=True, verbose_name="요청타입")
  author = models.ForeignKey("users.user",on_delete=models.SET_NULL,blank=True,null=True, verbose_name="회원")
  answer = models.TextField(blank=True,null=True, verbose_name="답변")
