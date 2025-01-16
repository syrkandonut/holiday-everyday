from django.db.models import (
    TextField,
)

from .base import Base


class Review(Base):
    text: TextField = TextField()

    class Meta:
        db_table = "reviews"