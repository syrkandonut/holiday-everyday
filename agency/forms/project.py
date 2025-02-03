from django.forms import ClearableFileInput, ImageField, ModelForm

from agency.models import Project


class ProjectMultipleFileForm(ModelForm):
    images = ImageField(
        widget=ClearableFileInput(attrs={"multiple": True}), label="Картинки"
    )

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
