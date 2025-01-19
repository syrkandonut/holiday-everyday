from django.db.models import (
    CharField,
    ManyToManyField,
    TextField,
)

from .base import Base
from .tag import Tag

PROJECT_TYPES = (
    ("WEDDING", "Свадьба"),
    ("CORPORATE", "Корпоратив"),
    ("PRIVATE", "Частное"),
)


class Project(Base):
    preview_image: CharField = CharField(max_length=512, verbose_name="Превью проекта")
    title: CharField = CharField(max_length=256, verbose_name="Заголовок проекта")
    descritpion: CharField = CharField(max_length=512, verbose_name="Описание проекта")
    customer: CharField = CharField(max_length=64, verbose_name="Заказчик проекта")
    place: CharField = CharField(
        max_length=64,
        verbose_name="Площадка проведения проекта",
    )
    photographer: CharField = CharField(max_length=64, verbose_name="Фотограф")
    video_url: CharField = CharField(
        max_length=512,
        verbose_name="Ссылка на видео проекта",
    )
    full_description: TextField = TextField(
        verbose_name="Полное описание проекта",
    )
    type: CharField = CharField(
        choices=PROJECT_TYPES,
        max_length=64,
        verbose_name="Тип проекта",
        default=PROJECT_TYPES[0][0],
    )
    tags: ManyToManyField = ManyToManyField(
        Tag,
        related_name="projects",
        verbose_name="Тэги проекта",
    )

    class Meta:
        db_table = "projects"
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return f"Проект {self.title}"
