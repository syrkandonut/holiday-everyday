from django.db.models import (
    CASCADE,
    CharField,
    ForeignKey,
)

from .base import Base
from .project import Project


class Image(Base):
    name: CharField = CharField(max_length=256)

    class Meta:
        db_table = "images"