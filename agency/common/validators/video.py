from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def rutube_url_validator(url: str):
    url_prefix = "https://rutube.ru/video"

    if not url.startswith(url_prefix):
        raise ValidationError(
            _(f"Ссылка должна начинаться с {url_prefix}"),
            params={"value": url},
        )
