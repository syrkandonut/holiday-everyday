from django.db.models import (
    CASCADE,
    CharField,
    ForeignKey,
)

from .base import Base
from .project import Project


class Image(Base):
    name: CharField = CharField(max_length=256, verbose_name="Название картинки")
    project: ForeignKey = ForeignKey(
        Project, related_name="images", on_delete=CASCADE, verbose_name="Проект"
    )

    class Meta:
        db_table = "images"
        verbose_name = "Картинку"
        verbose_name_plural = "Картинки"

    def __str__(self):
        return f"Картинка к проекту {self.project}"
