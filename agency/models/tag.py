from django.db.models import (
    CharField,
)

from .base import Base


class Tag(Base):
    name: CharField = CharField(
        max_length=64,
        verbose_name="Название тэга",
        unique=True,
    )

    class Meta:
        db_table = "tags"
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.capitalize()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"# {self.name}"
