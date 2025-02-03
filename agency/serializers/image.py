from rest_framework.serializers import ModelSerializer

from agency.models import Image
from config.settings import IMAGE_URL, SERVER_URI, STORAGE_IMAGE_PATH


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "name"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["name"] = (
            SERVER_URI
            + IMAGE_URL
            + str(data["name"]).replace("/" + STORAGE_IMAGE_PATH + "/", str())
        )

        return data
