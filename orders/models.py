from django.db import models
from cores import models as core_models

# Create your models here.


class Order(core_models.TimeStampedModel):
    class Meta:
        verbose_name = "주문"
        verbose_name_plural = "주문 모음"
        ordering = ["-created"]

    ORDER_CHOICES = (
        ("paid", "승인"),
        ("ready", "준비"),
        ("accountready", "계좌이체준비"),
        ("failed", "실패"),
        ("cancelled", "취소"),
    )
    PG_TYPE = (
        ("kakaopay", "카카오페이"),
        ("html5_inicis", "이니시스"),
    )
    user = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, related_name="orderuser"
    )
    seat = models.ForeignKey(
        "seats.Seat", on_delete=models.SET_NULL, null=True, related_name="orderseat"
    )
    buyer_name = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="구매자이름"
    )
    buyer_tel = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="구매자전화번호"
    )
    howmanyDate = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="주문일수",
    )
    merchant_uid = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="구매번호",
        help_text="수기 입력은 빈칸",
    )
    imp_uid = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="아임포트구매번호"
    )
    paid_at = models.PositiveIntegerField(null=True, blank=True, verbose_name="승인일시")
    pg_provider = models.CharField(
        choices=PG_TYPE, max_length=100, null=True, blank=True, verbose_name="PG사"
    )
    pg_tid = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="PG승인일시"
    )
    receipt_url = models.CharField(
        max_length=300, null=True, blank=True, verbose_name="영수증"
    )
    status = models.CharField(
        max_length=100,
        choices=ORDER_CHOICES,
        default="ready",
        null=True,
        blank=True,
        verbose_name="결재상태",
    )
    amount = models.PositiveIntegerField(null=True, blank=True, verbose_name="총결재금액")
