from django.db.models import CASCADE, OneToOneField, TextField

from .base import Base


class Review(Base):
    text: TextField = TextField(verbose_name="Текст отзыва")
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

    def __str__(self):
        return f"Отзыв проекта {self.project}"
