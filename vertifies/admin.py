from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Vertifie)
class SaladAdmin(admin.ModelAdmin):
    list_display = (
        "phone",
        "code",
    )
