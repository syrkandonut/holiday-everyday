from django.core.exceptions import ValidationError
from django.db.models import CASCADE, OneToOneField, TextField, URLField
from django.utils.translation import gettext_lazy as _

from .base import Base


def rutube_url_validator(url: str):
    url_prefix = "https://rutube.ru/video"

    if not url.startswith(url_prefix):
        raise ValidationError(
            _(f"Ссылка должна начинаться с {url_prefix}"),
            params={"value": url},
        )


class Review(Base):
    text: TextField = TextField(verbose_name="Текст отзыва")
    video: URLField = URLField(
        max_length=512,
        verbose_name="Видео отзыва с Rutube",
        validators=[rutube_url_validator],
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
        self.video = self.video.replace("?" + share_postfix, "")
        self.video = self.video.replace("r=plwd", "")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Отзыв проекта {self.project}"
