from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Alram)
class AlramAdmin(admin.ModelAdmin):

    list_display = [
        "headings",
        "subtitle",
        "updated",
        "created"
    ]
    readonly_fields = (
        "to",
        "senttime",
        "headings",
        "subtitle",
        "contents",
        "sented",
        "created",
        "updated"
    )
    fields = (
        "headings",
        "subtitle",
        "contents",
        "sented",
        "senttime",
        "to",
        "created",
        "updated"
    )
    # list_display_links = [
    #     "menu",
    # ]
    search_fields = ("=alram_headings",)
