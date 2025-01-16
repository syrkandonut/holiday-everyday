from django.db.models import CASCADE, ForeignKey, TextField

from .base import Base
from .project import Project


class Review(Base):
    text: TextField = TextField(verbose_name="Текст отзыва")
    project: ForeignKey = ForeignKey(
        Project,
        related_name="review",
        on_delete=CASCADE,
        verbose_name="Проект",
    )

    class Meta:
        db_table = "reviews"
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return "Отзыв проекта"
