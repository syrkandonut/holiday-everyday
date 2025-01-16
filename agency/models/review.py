from django.db.models import CASCADE, ForeignKey, TextField

from .base import Base


class Review(Base):
    text: TextField = TextField(verbose_name="Текст отзыва")

    class Meta:
        db_table = "reviews"
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return "Отзыв проекта"
