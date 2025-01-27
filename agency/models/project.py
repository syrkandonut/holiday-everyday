from django.db.models import (
    BooleanField,
    CharField,
    ImageField,
    ManyToManyField,
    TextField,
    URLField,
)

from agency.common.validators.video import rutube_url_validator
from config.settings import STORAGE_IMAGE_PATH

from .base import Base
from .tag import Tag

PROJECT_TYPES = (
    ("WEDDING", "Свадьба"),
    ("CORPORATE", "Корпоратив"),
    ("PRIVATE", "Частное"),
)


class Project(Base):
    preview_image: ImageField = ImageField(
        upload_to=STORAGE_IMAGE_PATH,
        verbose_name="Превью проекта",
        max_length=512,
    )
    title: CharField = CharField(max_length=256, verbose_name="Заголовок проекта")
    description: CharField = CharField(max_length=512, verbose_name="Описание проекта")
    customer: CharField = CharField(max_length=64, verbose_name="Заказчик проекта")
    place: CharField = CharField(
        max_length=64,
        verbose_name="Площадка проведения проекта",
    )
    photographer: CharField = CharField(max_length=64, verbose_name="Фотограф")
    video: URLField = URLField(
        max_length=512,
        verbose_name="Ссылка на видео проекта с Rutube",
        validators=[rutube_url_validator],
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

    published: BooleanField = BooleanField(verbose_name="Опубликовано", default=False)

    class Meta:
        db_table = "projects"
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def save(self, *args, **kwargs):
        share_postfix = "r=plwd"
        self.video = self.video.replace("?" + share_postfix, str())
        self.video = self.video.replace("r=plwd", str())

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Проект {self.title}"
