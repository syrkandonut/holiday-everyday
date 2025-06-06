from adminsortable.admin import SortableMixin  # type: ignore
from django.db.models import (
    CASCADE,
    ForeignKey,
    ImageField,
    PositiveIntegerField,
)

from agency.utils.img_converter import to_webp_and_thumbnail
from config.settings import STORAGE_IMAGE_PATH

from .base import Base


class Image(Base, SortableMixin):
    name: ImageField = ImageField(
        upload_to=STORAGE_IMAGE_PATH,
        verbose_name="Изображение",
        max_length=512,
    )

    project: ForeignKey = ForeignKey(
        "agency.Project",
        related_name="images",
        on_delete=CASCADE,
        verbose_name="Проект",
    )

    order: PositiveIntegerField = PositiveIntegerField(default=0, db_index=True)

    class Meta:
        db_table = "images"
        verbose_name = "Картинка проекта"
        verbose_name_plural = "Картинки проектов"
        ordering = ["order"]

    def save(self, *args, **kwargs):
        if self.name:
            to_webp_and_thumbnail(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
