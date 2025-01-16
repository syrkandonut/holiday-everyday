from django.db.models import (
    CharField,
)

from .base import Base


class Media(Base):
    title: CharField = CharField(max_length=256, verbose_name="Заголовок")
    media: CharField = CharField(max_length=256, verbose_name="Название источника")
    media_link: CharField = CharField(
        max_length=256,
        verbose_name="Ссылка на сайт источника",
    )
    preview_image: CharField = CharField(
        max_length=512,
        verbose_name="Ссылка на картинку для отображения",
    )
    preview_link: CharField = CharField(
        max_length=512,
        verbose_name="Ссылка на сайт для вставки",
    )

    class Meta:
        db_table = "medias"
        verbose_name = "СМИ"
        verbose_name_plural = "СМИ"

    def __str__(self):
        return f"СМИ {self.media}"
