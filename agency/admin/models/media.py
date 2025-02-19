from django.contrib import admin
from django.utils.html import format_html

from config.settings import IMAGE_URL, SERVER_URI, STORAGE_IMAGE_PATH


class MediaAdmin(admin.ModelAdmin):
    list_display = ("title", "name", "get_thumbnail")
    readonly_fields = ["get_thumbnail"]
    ordering = ["-date"]

    def get_thumbnail(self, obj):
        if obj.preview_image:
            image_url = (
                f"{SERVER_URI}{IMAGE_URL}"
                + f"{obj.preview_image.name.replace(STORAGE_IMAGE_PATH, str())}"
            )
            return format_html(
                '<img src="{}" style="width: 100px; height: auto;" />', image_url
            )

        return str()

    get_thumbnail.short_description = "Превью СМИ"  # type: ignore
