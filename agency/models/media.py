import io
import os

import PIL.Image
from django.core.files.base import ContentFile
from django.db.models import (
    CharField,
    DateField,
    ImageField,
    URLField,
)

from agency.models.image import IMG_BIG_SIZE, IMG_SMALL_SIZE
from config.settings import STORAGE_IMAGE_PATH

from .base import Base


class Media(Base):
    title: CharField = CharField(max_length=256, verbose_name="Заголовок статьи")
    name: CharField = CharField(max_length=256, verbose_name="Название СМИ")
    link: URLField = URLField(
        max_length=512,
        verbose_name="Ссылка на статью",
    )
    date: DateField = DateField(verbose_name="Дата публикации статьи")
    preview_image: ImageField = ImageField(
        upload_to=STORAGE_IMAGE_PATH,
        max_length=512,
        verbose_name="Картинка СМИ",
    )
    screenshot: ImageField = ImageField(
        upload_to=STORAGE_IMAGE_PATH,
        max_length=512,
        verbose_name="Скриншот статьи",
    )

    class Meta:
        db_table = "medias"
        verbose_name = "СМИ"
        verbose_name_plural = "СМИ"

    def save(self, *args, **kwargs):
        prew_image_pil = PIL.Image.open(self.preview_image)

        prew_image_io = io.BytesIO()

        prew_image_pil.thumbnail(IMG_BIG_SIZE)
        prew_image_pil.save(prew_image_io, format="WEBP")
        prew_image_io.seek(0)

        prew_image_name = f"{os.path.splitext(self.preview_image.name)[0]}.webp"
        prew_image_content_file = ContentFile(prew_image_io.read())

        self.preview_image.save(prew_image_name, prew_image_content_file, save=False)

        prew_image_io_thumb = io.BytesIO()
        prew_image_pil.thumbnail(IMG_SMALL_SIZE)
        prew_image_pil.save(prew_image_io_thumb, format="WEBP")
        prew_image_io_thumb.seek(0)

        prew_image_name_thumb = (
            f"{os.path.splitext(self.preview_image.name)[0]}_144p.webp"
        )

        with open(prew_image_name_thumb, "wb") as f:
            f.write(prew_image_io_thumb.read())

        scr_image_pil = PIL.Image.open(self.screenshot)

        scr_image_io = io.BytesIO()

        scr_image_pil.thumbnail(IMG_BIG_SIZE)
        scr_image_pil.save(scr_image_io, format="WEBP")
        scr_image_io.seek(0)

        scr_image_name = f"{os.path.splitext(self.screenshot.name)[0]}.webp"
        scr_image_content_file = ContentFile(scr_image_io.read())

        self.screenshot.save(scr_image_name, scr_image_content_file, save=False)

        scr_image_io_thumb = io.BytesIO()
        scr_image_pil.thumbnail(IMG_SMALL_SIZE)
        scr_image_pil.save(scr_image_io_thumb, format="WEBP")
        scr_image_io_thumb.seek(0)

        image_name_thumb = f"{os.path.splitext(self.screenshot.name)[0]}_144p.webp"

        with open(image_name_thumb, "wb") as f:
            f.write(scr_image_io_thumb.read())

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
