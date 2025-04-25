from adminsortable.admin import SortableTabularInline  # type: ignore
from django.contrib.admin import StackedInline
from django.urls import reverse
from django.utils.html import format_html

from agency.models import Image, Review
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
            return format_html(
                '<img src="{}" style="width: 100px; height: auto;" />', image_url
            )

        return str()

    def delete_button(self, obj):
        return format_html(
            '<a class="button" href="{}" '
            'style="background-color: #ba2121; color: white;"'
            ">Удалить</a>",
            reverse("admin:agency_delete_image", args=[obj.pk]),
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
