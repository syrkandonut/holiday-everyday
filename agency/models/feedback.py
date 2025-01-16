from django.db.models import (
    CharField,
    TextField,
)

from .base import Base


class Feedback(Base):
    name: CharField = CharField(max_length=64, verbose_name="Имя пользователя")
    phone: CharField = CharField(max_length=64, verbose_name="Телефонный номер")
    text: TextField = TextField(verbose_name="Текст обратной связи")

    class Meta:
        db_table = "feedbacks"
        verbose_name = "Обратную связь"
        verbose_name_plural = "Обратная связь"

    def __str__(self):
        return f"Обратная связь от {self.name}"
