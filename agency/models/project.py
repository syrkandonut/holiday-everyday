import os
import re
from urllib.parse import unquote

from django.db.models import (
    BooleanField,
    CharField,
    DateTimeField,
    ImageField,
    ManyToManyField,
    URLField,
)
from django_ckeditor_5.fields import CKEditor5Field

from agency.common.validators.video import rutube_url_validator
from agency.utils.img_converter import to_webp
from config.settings import (
    SERVER_URI,
    STORAGE_CKEDITOR_IMAGE_PATH,
    STORAGE_IMAGE_PATH,
)

from .base import Base
from .tag import Tag

PROJECT_TYPES = (
    ("WEDDING", "Свадьба"),
    ("CORPORATE", "Корпоратив"),
    ("PRIVATE", "Личные праздники"),
)


class Project(Base):
    preview_image: ImageField = ImageField(
        upload_to=STORAGE_IMAGE_PATH,
        verbose_name="Превью проекта",
        max_length=512,
        null=True,
        blank=True,
    )
    title: CharField = CharField(
        max_length=256,
        verbose_name="Заголовок проекта",
        null=True,
        blank=True,
    )
    description: CharField = CharField(
        max_length=512,
        verbose_name="Описание проекта",
        null=True,
        blank=True,
    )
    customer: CharField = CharField(
        max_length=64,
        verbose_name="Заказчик проекта",
        null=True,
        blank=True,
    )
    place: CharField = CharField(
        max_length=64,
        verbose_name="Площадка проведения проекта",
        null=True,
        blank=True,
    )
    photographer: CharField = CharField(
        max_length=64,
        verbose_name="Фотограф",
        null=True,
        blank=True,
    )
    video: URLField = URLField(
        max_length=512,
        verbose_name="Ссылка на видео проекта с Rutube",
        validators=[rutube_url_validator],
        null=True,
        blank=True,
    )
    full_description: CKEditor5Field = CKEditor5Field(
        verbose_name="Полное описание проекта",
        null=True,
        blank=True,
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
        blank=True,
    )
    published: BooleanField = BooleanField(verbose_name="Опубликовано", default=False)
    created_at: DateTimeField = DateTimeField(
        verbose_name="Дата и время создания",
        auto_now_add=True,
    )

    def publish(self):
        self.is_published = True
        self.save()

    def unpublish(self):
        self.is_published = False
        self.save()

    class Meta:
        db_table = "projects"
        ordering = ["-created_at"]

        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def save(self, *args, **kwargs):
        if self.video:
            share_postfix = "r=plwd"
            self.video = self.video.replace("?" + share_postfix, str())
            self.video = self.video.replace("r=plwd", str())

        if self.preview_image:
            to_webp(self.preview_image)

        if self.full_description:
            self.check_file_system_image_matches()
            self.reformat_full_description(self.full_description)

        super().save(*args, **kwargs)

    def check_file_system_image_matches(
        self, exclude_files: list[str] = [".gitignore"]
    ):
        images: list[str] = list()

        for proj in Project.objects.all():
            if Project.full_description:
                image = self.get_image_from_full_description(
                    full_description=proj.full_description
                )
                images.extend(image) if image else ...

        images.extend(
            self.get_image_from_full_description(full_description=self.full_description)
        )

        if not images:
            for file in os.listdir(STORAGE_CKEDITOR_IMAGE_PATH):
                if file not in exclude_files:
                    return os.unlink(os.path.join(STORAGE_CKEDITOR_IMAGE_PATH, file))

        for file in os.listdir(STORAGE_CKEDITOR_IMAGE_PATH):
            file_path = os.path.join(STORAGE_CKEDITOR_IMAGE_PATH, file)
            if file not in images:
                try:
                    if file not in exclude_files:
                        os.unlink(file_path)
                except FileNotFoundError:
                    pass

    def reformat_full_description(self, full_description: str) -> None:
        pattern = (
            r'<img([^>]*)style="[^"]*"([^>]*)'
            + r'src="([^"]*)"([^>]*)width="[^"]*"([^>]*)'
            + r'height="[^"]*"([^>]*)>'
        )
        replacement = r'<img\1\2src="{}\3"\4\5\6>'.format(SERVER_URI)
        self.full_description = re.sub(pattern, replacement, full_description)

    @staticmethod
    def get_image_from_full_description(full_description: str) -> list:
        pattern = r'src=["\'][^"\']*/([^/"\']+)["\']'

        return re.findall(pattern, unquote(full_description))

    def __str__(self):
        return f"Проект {self.title}"
