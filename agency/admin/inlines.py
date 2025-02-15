from django.contrib.admin import StackedInline, TabularInline
from django.utils.html import format_html

from agency.models import Image, Review
from config.settings import IMAGE_URL, SERVER_URI, STORAGE_IMAGE_PATH


class ImageInLine(TabularInline):
    model = Image
    extra = 0
    fields = ["name", "get_thumbnail"]
    ordering = ["-created_at"]

    readonly_fields = ["get_thumbnail"]

    def get_thumbnail(self, obj):
        if obj.name:
            image_url = (
                f"{SERVER_URI}{IMAGE_URL}"
                + f"{obj.name.name.replace(STORAGE_IMAGE_PATH, str())}"
            )
            return format_html(
                '<img src="{}" style="width: 100px; height: auto;" />', image_url
            )

        return str()

    get_thumbnail.short_description = "Картинка"  # type: ignore


# Deprecated 07.02.2025 according to the requirements
class ReviewInLine(StackedInline):
    model = Review

    min_num = 1
    max_num = 1
