from django.db.models import (
    CharField,
    DateField,
    ImageField,
    URLField,
)

from agency.utils.img_converter import to_webp, to_webp_and_thumbnail
from config.settings import STORAGE_IMAGE_PATH

from .base import Base


class Media(Base):
    title: CharField = CharField(
        max_length=256,
        verbose_name="Заголовок статьи",
        null=True,
        blank=True,
    )
    name: CharField = CharField(
        max_length=256,
        verbose_name="Название СМИ",
        null=True,
        blank=True,
    )
    link: URLField = URLField(
        max_length=512,
        verbose_name="Ссылка на статью",
        null=True,
        blank=True,
    )
    date: DateField = DateField(
        verbose_name="Дата публикации статьи",
        null=True,
        blank=True,
    )
    preview_image: ImageField = ImageField(
        upload_to=STORAGE_IMAGE_PATH,
        max_length=512,
        verbose_name="Картинка СМИ",
        null=True,
        blank=True,
    )
    screenshot: ImageField = ImageField(
        upload_to=STORAGE_IMAGE_PATH,
        max_length=512,
        verbose_name="Скриншот статьи",
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "medias"
        verbose_name = "СМИ"
        verbose_name_plural = "СМИ"

    def save(self, *args, **kwargs):
        if self.preview_image:
            to_webp_and_thumbnail(self.preview_image)

        if self.screenshot:
            to_webp(self.screenshot)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
