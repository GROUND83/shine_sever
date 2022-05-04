from dataclasses import fields
from django.contrib import admin
from . import models
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin


@admin.register(models.UserType)
class ItemAdmin(admin.ModelAdmin):

    """Item Admin Definition"""

    list_display = ("name",)

    # def used_by(self, obj):
    #     return obj.rooms.count()

    pass


# Register your models here.
@admin.register(models.User)
class CustomUserAdmin(
    admin.ModelAdmin,
):
    def image_tag(self, obj):
        if obj.user_image:
            return format_html(
                '<img src="{}" style="width:150px;height:150px"/>'.format(
                    obj.user_image.url
                )
            )
        else:
            return format_html('<img src="" />')

    image_tag.short_description = "Image"

    list_display = (
        "id",
        "username",
        "phone",
        "user_type",
        "personalPolicy",
        "timeAlram",
        "eventAlram",
    )
    readonly_fields = ("image_tag",)
    fields = (
        "image_tag",
        "username",
        "phone",
        "gender",
        "password",
        "user_type",
        "user_birth",
        "school_name",
        "school_grade",
        "timeAlram",
        "eventAlram",
        "personalPolicy",
        "user_image",
        "deviceId",
        "onsignalId",
    )
    search_fields = ["username", "phone"]
