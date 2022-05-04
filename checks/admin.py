from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = [
        "seatName",
        "seatUser",
        "check_type",
        "created"
    ]

    # list_display_links = [
    #     "menu",
    # ]
    search_fields = ("=check_seatName",)