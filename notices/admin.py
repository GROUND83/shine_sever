from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Notice)
class NotiveAdmin(admin.ModelAdmin):

    list_display = [
        "title",
        "updated",
    ]

    # list_display_links = [
    #     "menu",
    # ]
    search_fields = ("=notice_title",)
