from django.db.models import (
    CharField,
)

from .base import Base


class Media(Base):
    title: CharField = CharField(max_length=256)
    media: CharField = CharField(max_length=256)
    media_link: CharField = CharField(max_length=256)
    preview_image: CharField = CharField(max_length=512)
    preview_link: CharField = CharField(max_length=512)


    class Meta:
        db_table = "medias"