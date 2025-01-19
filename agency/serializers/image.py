from rest_framework.serializers import ModelSerializer

from agency.models import Image


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ["name"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["name"] = str(data["name"]).lstrip("data/images/")
        return data
