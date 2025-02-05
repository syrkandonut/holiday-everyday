from django.db.models import CASCADE, ImageField, OneToOneField, TextField, URLField

from agency.common.validators.video import rutube_url_validator
from agency.utils.img_converter import to_webp_and_thumbnail
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
        if self.video:
            share_postfix = "r=plwd"
            self.video = self.video.replace("?" + share_postfix, str())
            self.video = self.video.replace("r=plwd", str())

        to_webp_and_thumbnail(self.preview_image)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Отзыв к {self.project}"
