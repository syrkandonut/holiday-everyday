from rest_framework.serializers import ModelSerializer

from agency.models import Image


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "name"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["name"] = "http://localhost:1234/media/" + str(data["name"]).lstrip(
            "data/images/"
        )
        return data
