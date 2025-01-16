from django.db.models import (
    CASCADE,
    CharField,
    ManyToManyField,
    OneToOneField,
    TextField
)

from .base import Base
from .review import Review
from .tag import Tag

PROJECT_TYPES = (
    ("WEDDING", "WEDDING"),
    ("CORPORATE", "CORPORATE"),
    ("PRIVATE", "PRIVATE"),
)


class Project(Base):
    preview_image: CharField = CharField(max_length=512)
    title: CharField = CharField(max_length=256)
    descritpion: CharField = CharField(max_length=512)
    customer: CharField = CharField(max_length=64)
    place: CharField = CharField(max_length=64)
    photographer: CharField = CharField(max_length=64)
    video_url: CharField = CharField(max_length=512)
    full_description: TextField = TextField()
    type: CharField = CharField(choices=PROJECT_TYPES, max_length=64)
    tags: ManyToManyField = ManyToManyField(Tag, related_name="projects")
    review: OneToOneField = OneToOneField(Review, on_delete=CASCADE)

    class Meta:
        db_table = "projects"