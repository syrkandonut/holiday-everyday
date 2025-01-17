from rest_framework.serializers import ModelSerializer

from agency.models import Image


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ["name", "image"]
