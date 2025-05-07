from adminsortable.admin import SortableTabularInline  # type: ignore
from django.contrib.admin import StackedInline
from django.urls import reverse

from agency.models import Image, Review
from agency.utils.as_html import HTMLColor, html_get_button, html_get_thumbnail
from config.settings import IMAGE_URL, SERVER_URI, STORAGE_IMAGE_PATH


class ImageInLine(SortableTabularInline):
    model = Image
    extra = 0
    classes = ["collapse"]

    fields = ["name", "get_thumbnail", "delete_button"]
    readonly_fields = ["get_thumbnail", "delete_button"]
    can_delete = False

    ordering = ["order"]

    def get_thumbnail(self, obj):
        if obj.name:
            image_url = (
                f"{SERVER_URI}{IMAGE_URL}"
                + f"{obj.name.name.replace(STORAGE_IMAGE_PATH, str())}"
            )
            return html_get_thumbnail(image_url)

        return str()

    def delete_button(self, obj):
        return html_get_button(
            button_color=HTMLColor.RED,
            button_text="Удалить",
            text_color=HTMLColor.WHITE,
            source_url=reverse("admin:agency_delete_image", args=[obj.pk]),
        )

    # def has_add_permission(self, request, obj=None):
    #     return False

    get_thumbnail.short_description = "Картинка"  # type: ignore
    delete_button.short_description = "Удалить"  # type: ignore


# Deprecated 07.02.2025 according to the requirements
class ReviewInLine(StackedInline):
    model = Review

    min_num = 1
    max_num = 1
