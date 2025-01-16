from django.db.models import (
    CharField,
)

from .base import Base

TAGS = (
    ("NATURE", "Природа"),
    ("COUNTRYSIDE", "Сельская местность"),
    ("FOREST", "Лес"),
    ("WATERSIDE", "Берег моря"),
    ("MOUNTAINS", "Горы"),
    ("ABROAD", "За границей"),
    ("ESTATE", "Поместье"),
    ("VILLA", "Вилла"),
    ("RESTAURANT", "Ресторан"),
)


class Tag(Base):
    name: CharField = CharField(
        max_length=64, choices=TAGS, verbose_name="Название тэга"
    )

    class Meta:
        db_table = "tags"
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        for TAG, MAPPING in TAGS:
            if self.name == TAG:
                RU_TAG = MAPPING
                break

        return f"# {RU_TAG}"
