from rest_framework.serializers import CharField, Serializer


class EmailDataSerializer(Serializer):
    name = CharField(min_length=1, max_length=64, required=True)
    phone = CharField(required=True)
    text = CharField(min_length=1, max_length=512, required=True)
