from rest_framework.serializers import ModelSerializer

from agency.models import Media
from config.settings import (
    IMAGE_URL,
    SERVER_URI,
    STORAGE_IMAGE_PATH,
)


class MediaSerializer(ModelSerializer):
    class Meta:
        model = Media
        fields = ["id", "title", "name", "link", "date", "preview_image", "screenshot"]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["preview_image"] = (
            SERVER_URI
            + IMAGE_URL
            + str(data["preview_image"])
            .replace("/" + STORAGE_IMAGE_PATH + "/", str())
            .replace(SERVER_URI, str())
        )

        data["screenshot"] = (
            SERVER_URI
            + IMAGE_URL
            + str(data["screenshot"])
            .replace("/" + STORAGE_IMAGE_PATH + "/", str())
            .replace(SERVER_URI, str())
        )

        return data
