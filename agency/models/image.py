from django.db.models import (
    CASCADE,
    ForeignKey,
    ImageField,
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .base import Base

def validator(value: str):
    if Image.objects.filter(name=value).exists():
        raise ValidationError(
            _("%(value)s Уже существует"),
            params={"value": value},
        )
    
class Image(Base):
    name: ImageField = ImageField(
        upload_to="data/images",
        verbose_name="Изображение",
        unique=True,
        validators=[validator]
    )

    project: ForeignKey = ForeignKey(
        "agency.Project",
        related_name="images",
        on_delete=CASCADE,
        verbose_name="Проект",
    )

    def save(self, *args, **kwargs):
        if self.name:
            self.name = str(self.name)
            super().save(*args, **kwargs)

    class Meta:
        db_table = "images"
        verbose_name = "Картинку"
        verbose_name_plural = "Картинки"

    def __str__(self):
        return f"Картинка к проекту {self.project}"
