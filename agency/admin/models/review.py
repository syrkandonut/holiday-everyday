from django.contrib import admin

from agency.utils.as_html import html_get_thumbnail
from config.settings import IMAGE_URL, SERVER_URI, STORAGE_IMAGE_PATH


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("get_project", "get_thumbnail")
    readonly_fields = ["get_thumbnail"]

    def get_project(sellf, obj):
        return obj

    def get_thumbnail(self, obj):
        if obj.preview_image:
            image_url = (
                f"{SERVER_URI}{IMAGE_URL}"
                + f"{obj.preview_image.name.replace(STORAGE_IMAGE_PATH, str())}"
            )
            return html_get_thumbnail(image_url)

        return str()

    get_project.short_description = "Отзыв"  # type: ignore
    get_thumbnail.short_description = "Превью отзыва"  # type: ignore
