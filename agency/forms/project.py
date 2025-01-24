from django.forms import ModelForm

from agency.models import Project

from .multiple import MultipleFileField


class ProjectMultipleFileForm(ModelForm):
    images = MultipleFileField(label="Картинки")

    class Meta:
        model = Project
        fields = [
            "preview_image",
            "title",
            "description",
            "customer",
            "place",
            "photographer",
            "video",
            "full_description",
            "type",
            "tags",
        ]
