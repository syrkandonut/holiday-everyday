from adminsortable.admin import SortableAdmin  # type: ignore
from django.contrib.admin import display
from django.db.models import ManyToManyField
from django.forms import CheckboxSelectMultiple
from django.shortcuts import get_object_or_404, redirect
from django.urls import path, reverse

from agency.admin.inlines import ImageInLine
from agency.forms import ProjectMultipleFileForm
from agency.models import Image, Project
from agency.utils.as_html import (
    HTMLColor,
    html_get_button,
    html_get_preview_with_thumbnail,
    html_get_preview_without_thumbnail,
)
from config.settings import IMAGE_URL, SERVER_URI, STORAGE_IMAGE_PATH


class ProjectAdmin(SortableAdmin):
    inlines = [ImageInLine]
    form = ProjectMultipleFileForm
    list_display = ("title", "get_preview", "publish_button")
    readonly_fields = ["get_preview", "delete_all_images_button"]
    formfield_overrides = {
        ManyToManyField: {"widget": CheckboxSelectMultiple},
    }
    ordering = ["-created_at"]

    @display(description="Действие")
    def publish_button(self, obj):
        if not (obj.title and obj.preview_image):
            return "Недоступно для публикации, добавьте заголовок и превью"

        if obj.published:
            button_text = "Снять с публикации"
            button_color = HTMLColor.GREY
        else:
            button_text = "Опубликовать"
            button_color = HTMLColor.GREEN

        return html_get_button(
            button_color=button_color,
            button_text=button_text,
            text_color=HTMLColor.WHITE,
            source_url=reverse("admin:agency_toggle_publish", args=[obj.pk]),
        )

    def toggle_publish(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        project.published = not project.published
        project.save()
        return redirect(reverse("admin:agency_project_changelist"))

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "delete_image/<str:image_id>/",
                self.admin_site.admin_view(self.delete_image),
                name="agency_delete_image",
            ),
            path(
                "delete_all_images/<str:project_id>/",
                self.admin_site.admin_view(self.delete_all_images),
                name="agency_delete_all_images",
            ),
            path(
                "toggle_publish/<str:project_id>/",
                self.admin_site.admin_view(self.toggle_publish),
                name="agency_toggle_publish",
            ),
        ]
        return custom_urls + urls

    def delete_image(self, request, image_id):
        image = get_object_or_404(Image, pk=image_id)
        project_id = image.project.pk
        image.delete()
        self.message_user(request, f"Картинка {image.name.name} удалена.")
        return redirect(reverse("admin:agency_project_change", args=[project_id]))

    def delete_all_images(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        Image.objects.filter(project=project).delete()
        self.message_user(request, f"Все картинки проекта {project.title} удалены.")
        return redirect(reverse("admin:agency_project_change", args=[project_id]))

    def get_preview(self, obj):
        if obj.preview_image:
            image_url = (
                f"{SERVER_URI}{IMAGE_URL}"
                + f"{obj.preview_image.name.replace(STORAGE_IMAGE_PATH, str())}"
            )
            return html_get_preview_with_thumbnail(
                project_id=obj.id,
                image_url=image_url,
            )

        if obj.title is None:
            return "Недоступен, добавьте заголовок проекта"

        if obj:
            return html_get_preview_without_thumbnail(
                project_id=obj.id, warning_text="<Без превью>"
            )

        return str()

    def delete_all_images_button(self, obj):
        return html_get_button(
            button_color=HTMLColor.RED,
            text_color=HTMLColor.WHITE,
            button_text="Удалить все картинки",
            source_url=reverse("admin:agency_delete_all_images", args=[obj.pk]),
        )

    get_preview.short_description = "Предпросмотр"  # type: ignore
    delete_all_images_button.short_description = "Удалить картинки"  # type: ignore

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        project = form.instance

        if request.FILES.getlist("images"):
            image_exists = list(
                Image.objects.filter(project=project).values_list("name", flat=True)
            )

            for image in request.FILES.getlist("images"):
                if str(image) not in image_exists:
                    Image.objects.create(project=project, name=image)
