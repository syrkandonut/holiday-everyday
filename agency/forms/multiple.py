from django.forms import ClearableFileInput, ImageField

# Deprecated with downgrade from Django 5 to Django 4.2

class MultipleImageInput(ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleImageInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result
