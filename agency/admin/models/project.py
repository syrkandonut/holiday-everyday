from adminsortable.admin import SortableAdmin
from django.db.models import ManyToManyField
from django.forms import CheckboxSelectMultiple
from django.shortcuts import get_object_or_404, redirect
from django.urls import path, reverse
from django.utils.html import format_html
from django.http import Http404
from agency.admin.actions import make_published, make_unpublished
from agency.admin.inlines import ImageInLine
from agency.forms import ProjectMultipleFileForm
from agency.models import Image
from agency.models.project import Project
from config.settings import IMAGE_URL, SERVER_URI, STORAGE_IMAGE_PATH


class ProjectAdmin(SortableAdmin):
    inlines = [ImageInLine]
    form = ProjectMultipleFileForm
    actions = [make_published, make_unpublished]
    list_display = ("title", "published", "get_thumbnail", "get_link")
    readonly_fields = ["get_thumbnail", "delete_all_images_button"]
    formfield_overrides = {
        ManyToManyField: {"widget": CheckboxSelectMultiple},
    }
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'delete_image/<str:image_id>/', #Keep original since that's what's used.
                self.admin_site.admin_view(self.delete_image),
                name='agency_delete_image', #Updated as these names must match
            ),
            path(
                'delete_all_images/<str:project_id>/',
                self.admin_site.admin_view(self.delete_all_images),
                name='agency_delete_all_images',
            ),
        ]
        return custom_urls + urls

    def delete_image(self, request, image_id):
        image = get_object_or_404(Image, pk=image_id)
        project_id = image.project.pk
        image.delete()
        self.message_user(request, f"Картинка {image.name.name} удалена.")
        return redirect(reverse('admin:agency_project_change', args=[project_id]))

    def delete_all_images(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        Image.objects.filter(project=project).delete()
        self.message_user(request, f"Все картинки проекта {project.title} удалены.")
        return redirect(reverse('admin:agency_project_change', args=[project_id]))

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
    
    def delete_all_images_button(self, obj):
        return format_html(
            '<a class="button" href="{}" style="background-color: #ba2120; color: white;">Удалить все картинки</a>',
            reverse('admin:agency_delete_all_images', args=[obj.pk])
        )

    def get_link(self, obj):
        if obj:
            return format_html(
                f'<a href="{SERVER_URI}/portfolio/{{}}/" target="_blank">{{}}</a>',
                obj.id,
                obj.title,
            )

        return str()

    get_thumbnail.short_description = "Превью"  # type: ignore
    get_link.short_description = "Предпросмотр"  # type: ignore
    delete_all_images_button.short_description = "Удалить картинки" # type: ignore

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
