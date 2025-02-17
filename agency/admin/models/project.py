from django.contrib import admin
from django.db.models import ManyToManyField
from django.forms import CheckboxSelectMultiple
from django.utils.html import format_html

from agency.admin.actions import make_published, make_unpublished
from agency.admin.inlines import ImageInLine
from agency.forms import ProjectMultipleFileForm
from agency.models import Image
from config.settings import IMAGE_URL, SERVER_URI, STORAGE_IMAGE_PATH


class ProjectAdmin(admin.ModelAdmin):
    inlines = [ImageInLine]
    form = ProjectMultipleFileForm
    actions = [make_published, make_unpublished]
    list_display = ("title", "published", "get_thumbnail", "get_link")
    readonly_fields = ["get_thumbnail"]
    formfield_overrides = {
        ManyToManyField: {"widget": CheckboxSelectMultiple},
    }

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
