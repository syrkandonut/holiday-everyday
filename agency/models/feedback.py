from django.core.exceptions import ValidationError
from django.db.models import (
    CharField,
    TextField,
)
from django.utils.translation import gettext_lazy as _

from .base import Base


def validate_phone(value: str):
    if not (value[0] not in ["7", "8", "+7"]):
        raise ValidationError(
            _("Номер начинаться с `7`, `8` или `+7`"),
            params={"value": value},
        )

    if len(value) > 12 or len(value) < 11:
        raise ValidationError(
            _("Длина номера должна соответствовать 11 < Длина < 12"),
            params={"value": value},
        )

    for i in value[1:]:
        if not i.isdigit():
            raise ValidationError(
                _("%(value)s Ошибка ввода номера, введены неккоректные символы"),
                params={"value": value},
            )


class Feedback(Base):
    name: CharField = CharField(max_length=64, verbose_name="Имя пользователя")
    phone: CharField = CharField(
        max_length=64, verbose_name="Телефонный номер", validators=[validate_phone]
    )
    text: TextField = TextField(verbose_name="Текст обратной связи")

    class Meta:
        db_table = "feedbacks"
        verbose_name = "Обратную связь"
        verbose_name_plural = "Обратная связь"

    def __str__(self):
        return f"Обратная связь от {self.name}"
