import io
import os

import PIL.Image
from django.core.files.base import ContentFile
from django.db.models import CASCADE, ImageField, OneToOneField, TextField, URLField

from agency.common.validators.video import rutube_url_validator
from agency.models.image import IMG_BIG_SIZE, IMG_SMALL_SIZE
from config.settings import STORAGE_IMAGE_PATH

from .base import Base


class Review(Base):
    text: TextField = TextField(verbose_name="Текст отзыва")
    preview_image: ImageField = ImageField(
        upload_to=STORAGE_IMAGE_PATH,
        max_length=512,
        verbose_name="Картинка к отзыву",
    )
    video: URLField = URLField(
        max_length=512,
        verbose_name="Ссылка на видео отзыва с Rutube",
        validators=[rutube_url_validator],
        null=True,
        blank=True,
    )
    project: OneToOneField = OneToOneField(
        "agency.Project",
        related_name="review",
        on_delete=CASCADE,
        verbose_name="Проект",
        unique=True,
    )

    class Meta:
        db_table = "reviews"
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def save(self, *args, **kwargs):
        share_postfix = "r=plwd"
        self.video = self.video.replace("?" + share_postfix, str())
        self.video = self.video.replace("r=plwd", str())

        image_pil = PIL.Image.open(self.preview_image)

        image_io = io.BytesIO()

        image_pil.thumbnail(IMG_BIG_SIZE)
        image_pil.save(image_io, format="WEBP")
        image_io.seek(0)

        image_name = f"{os.path.splitext(self.preview_image.name)[0]}.webp"
        image_content_file = ContentFile(image_io.read())

        self.preview_image.save(image_name, image_content_file, save=False)

        image_io_thumb = io.BytesIO()
        image_pil.thumbnail(IMG_SMALL_SIZE)
        image_pil.save(image_io_thumb, format="WEBP")
        image_io_thumb.seek(0)

        image_name_thumb = f"{os.path.splitext(self.preview_image.name)[0]}_144p.webp"

        with open(image_name_thumb, "wb") as f:
            f.write(image_io_thumb.read())

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Отзыв проекта {self.project}"
