import io
import os

import PIL.Image
from django.core.files.base import ContentFile
from django.db.models import (
    CASCADE,
    ForeignKey,
    ImageField,
)

from config.settings import STORAGE_IMAGE_PATH

from .base import Base

IMG_BIG_SIZE = (1280, 720)
IMG_SMALL_SIZE = (256, 144)


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
        image_pil = PIL.Image.open(self.name)

        image_io = io.BytesIO()

        image_pil.thumbnail(IMG_BIG_SIZE)
        image_pil.save(image_io, format="WEBP")
        image_io.seek(0)

        image_name = f"{os.path.splitext(self.name.name)[0]}.webp"
        image_content_file = ContentFile(image_io.read())

        self.name.save(image_name, image_content_file, save=False)

        image_io_thumb = io.BytesIO()
        image_pil.thumbnail(IMG_SMALL_SIZE)
        image_pil.save(image_io_thumb, format="WEBP")
        image_io_thumb.seek(0)

        image_name_thumb = f"{os.path.splitext(self.name.name)[0]}_144p.webp"

        with open(image_name_thumb, "wb") as f:
            f.write(image_io_thumb.read())

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.project.title} | {self.name}"
