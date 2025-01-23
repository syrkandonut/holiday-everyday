from uuid import uuid4

from django.db.models import Model, UUIDField


class Base(Model):
    id: UUIDField = UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        unique=True,
    )

    class Meta:
        abstract = True
