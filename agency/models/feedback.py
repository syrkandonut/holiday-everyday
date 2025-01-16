from django.db.models import (
    CharField,
    TextField,
)   

from .base import Base


class Feedback(Base):
    name: CharField = CharField(max_length=64)
    phone: CharField = CharField(max_length=64)
    text: TextField = TextField()
    
    class Meta:
        db_table = "feedbacks"
