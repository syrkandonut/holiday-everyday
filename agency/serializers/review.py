import re

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from agency.models import Review
from config.settings import (
    IMAGE_URL,
    SERVER_URI,
    SERVER_PORT,
    SERVER_URI,
    STORAGE_IMAGE_PATH,
)


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ["preview_image", "text", "video"]

    text = SerializerMethodField()

    def convert_to_nbsp(self, text) -> str:
        return re.sub(r"(\b\w{1,3}\b)\s", r"\1&nbsp;", text)

    def get_text(self, obj: Review):
        return self.convert_to_nbsp(obj.text)

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["preview_image"] = (
            SERVER_URI
            + IMAGE_URL
            + str(data["preview_image"])
            .replace("/" + STORAGE_IMAGE_PATH + "/", str())
            .replace(SERVER_URI.rstrip(f":{SERVER_PORT}"), str())
        )

        return data
