from django.contrib import admin
from django.db.models import ManyToManyField
from django.forms import CheckboxSelectMultiple
from django.utils.html import format_html

from agency.forms import ProjectMultipleFileForm
from agency.models import Image, Media, Project, Review, Tag
from config.settings import IMAGE_URL, SERVER_URI, STORAGE_IMAGE_PATH

from .actions import make_published, make_unpublished
from .inlines import ImageInLine, ReviewInLine


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ImageInLine, ReviewInLine]
    form = ProjectMultipleFileForm
    actions = [make_published, make_unpublished]
    list_display = ("title", "published", "get_link")

    formfield_overrides = {
        ManyToManyField: {"widget": CheckboxSelectMultiple},
    }

    def get_link(self, obj):
        return format_html(
            f'<a href="{SERVER_URI}/portfolio/{{}}/" target="_blank">{{}}</a>',
            obj.id,
            obj.title,
        )

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


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ["name"]


@admin.register(Image)
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
            return format_html(
                '<img src="{}" style="width: 100px; height: auto;" />', image_url
            )
        return ""

    get_name.short_description = "Название"  # type: ignore
    get_thumbnail.short_description = "Изображение"  # type: ignore


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("get_project", "get_thumbnail")

    def get_project(sellf, obj):
        return obj

    def get_thumbnail(self, obj):
        if obj.preview_image:
            image_url = (
                f"{SERVER_URI}{IMAGE_URL}"
                + f"{obj.preview_image.name.replace(STORAGE_IMAGE_PATH, str())}"
            )
            return format_html(
                '<img src="{}" style="width: 100px; height: auto;" />', image_url
            )

    get_project.short_description = "Отзыв"  # type: ignore
    get_thumbnail.short_description = "Превью отзыва"  # type: ignore


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ("name", "get_thumbnail")

    def get_thumbnail(self, obj):
        if obj.preview_image:
            image_url = (
                f"{SERVER_URI}{IMAGE_URL}"
                + f"{obj.preview_image.name.replace(STORAGE_IMAGE_PATH, str())}"
            )
            return format_html(
                '<img src="{}" style="width: 100px; height: auto;" />', image_url
            )

    get_thumbnail.short_description = "Превью СМИ"  # type: ignore
