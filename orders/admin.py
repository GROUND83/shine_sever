from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = [
        "user",
        "seat",
        "amount",
        "buyer_name",
        "buyer_tel",
        "howmanyDate",
        "merchant_uid",
        "imp_uid",
        "paid_at",
        "pg_tid",
        "receipt_url",
        "status",
    ]

    # list_display_links = [
    #     "menu",
    # ]
    search_fields = ("=user",)
