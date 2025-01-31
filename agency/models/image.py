from django.db.models import (
    CASCADE,
    ForeignKey,
    ImageField,
)

from agency.utils.img_converter import to_webp_and_save_thumbnail
from config.settings import STORAGE_IMAGE_PATH

from .base import Base


class Image(Base):
    name: ImageField = ImageField(
        upload_to=STORAGE_IMAGE_PATH,
        verbose_name="Изображение",
        unique=True,
    )

    project: ForeignKey = ForeignKey(
        "agency.Project",
        related_name="images",
        on_delete=CASCADE,
        verbose_name="Проект",
    )

    class Meta:
        db_table = "images"
        verbose_name = "Картинку"
        verbose_name_plural = "Картинки"

    def save(self, *args, **kwargs):
        to_webp_and_save_thumbnail(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.project.title} | {self.name}"
