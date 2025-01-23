import re

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from agency.models import Review


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ["text"]

    text = SerializerMethodField()

    def convert_text(self, text) -> str:
        return re.sub(r"(\b\w{1,3}\b)\s", r"\1&nbsp;", text)

    def get_text(self, obj: Review):
        return self.convert_text(obj.text)
