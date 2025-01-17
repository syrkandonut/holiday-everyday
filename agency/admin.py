from django import forms
from django.contrib import admin
from django.db.models import ManyToManyField
from django.forms import CheckboxSelectMultiple

from .models import Feedback, Image, Media, Project, Review, Tag


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class MultipleFileForm(forms.ModelForm):
    images = MultipleFileField(label="Картинки")

    class Meta:
        model = Project
        fields = [
            "preview_image",
            "title",
            "descritpion",
            "customer",
            "place",
            "photographer",
            "video_url",
            "full_description",
            "type",
            "tags",
        ]


class ImageInLine(admin.TabularInline):
    model = Image
    extra = 0
    fields = ["name"]


class ReviewInLine(admin.TabularInline):
    model = Review


class MultiplieImageInLine(admin.TabularInline):
    model = Image
    form = MultipleFileForm
    fields = ["images"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ImageInLine, ReviewInLine]
    form = MultipleFileForm
    formfield_overrides = {
        ManyToManyField: {"widget": CheckboxSelectMultiple},
    }

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        project = form.instance

        if request.FILES.getlist("images"):
            for image in request.FILES.getlist("images"):
                Image.objects.create(project=project, name=image)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ["name"]

    def has_add_permission(self, request):
        return "project" not in request.path


admin.site.register((Review, Feedback, Media, Image))
