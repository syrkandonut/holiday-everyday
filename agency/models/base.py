from django.db.models import AutoField, Model


class Base(Model):
    id: AutoField = AutoField(primary_key=True)

    class Meta:
        abstract = True