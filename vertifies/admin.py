from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Vertifie)
class VertifieAdmin(admin.ModelAdmin):
    list_display = (
        "phone",
        "code",
        "updated"
    )
    fields = (
        "phone",
        "code",
        "updated",
        "limitTime",
    )
    readonly_fields = ("updated",)

