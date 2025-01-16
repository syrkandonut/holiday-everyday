from django.db.models import (
    CharField,
)

from .base import Base


class Tag(Base):
    name: CharField = CharField(max_length=64)

    class Meta:
        db_table = "tags"
