from django.db.models import (
    CharField,
    DateField,
    ImageField,
    URLField,
)

from agency.utils.img_converter import to_webp_and_thumbnail, to_webp
from config.settings import STORAGE_IMAGE_PATH

from .base import Base


class Media(Base):
    title: CharField = CharField(max_length=256, verbose_name="Заголовок статьи")
    name: CharField = CharField(max_length=256, verbose_name="Название СМИ")
    link: URLField = URLField(
        max_length=512,
        verbose_name="Ссылка на статью",
    )
    date: DateField = DateField(verbose_name="Дата публикации статьи")
    preview_image: ImageField = ImageField(
        upload_to=STORAGE_IMAGE_PATH,
        max_length=512,
        verbose_name="Картинка СМИ",
    )
    screenshot: ImageField = ImageField(
        upload_to=STORAGE_IMAGE_PATH,
        max_length=512,
        verbose_name="Скриншот статьи",
    )

    class Meta:
        db_table = "medias"
        verbose_name = "СМИ"
        verbose_name_plural = "СМИ"

    def save(self, *args, **kwargs):
        to_webp_and_thumbnail(self.preview_image)
        to_webp(self.screenshot)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
