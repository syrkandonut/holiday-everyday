from django.db.models import CASCADE, OneToOneField, TextField, URLField

from agency.common.validators.video import rutube_url_validator

from .base import Base


class Review(Base):
    text: TextField = TextField(verbose_name="Текст отзыва")
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

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Отзыв проекта {self.project}"
