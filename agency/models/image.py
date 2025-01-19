from django.db.models import (
    CASCADE,
    ForeignKey,
    ImageField,
)

from .base import Base


class Image(Base):
    name: ImageField = ImageField(
        upload_to="data/images",
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

    def __str__(self):
        return f"Картинка к проекту {self.project}"
