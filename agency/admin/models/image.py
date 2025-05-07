from django.contrib import admin

from agency.utils.as_html import html_get_thumbnail
from config.settings import IMAGE_URL, SERVER_URI, STORAGE_IMAGE_PATH

# Deprecated 07.02.2025 according to the requirements


class ImageAdmin(admin.ModelAdmin):
    fields = ["name", "project"]
    list_display = ("get_name", "project", "get_thumbnail")

    def get_name(self, obj):
        if obj.name:
            return obj.name.name.replace(STORAGE_IMAGE_PATH + "/", str())
        return ""

    def get_thumbnail(self, obj):
        if obj.name:
            image_url = (
                f"{SERVER_URI}{IMAGE_URL}"
                + f"{obj.name.name.replace(STORAGE_IMAGE_PATH, str())}"
            )
            return html_get_thumbnail(image_url)

        return str()

    get_name.short_description = "Название"  # type: ignore
    get_thumbnail.short_description = "Изображение"  # type: ignore
