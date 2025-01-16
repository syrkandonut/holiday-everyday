from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.utils.serializer_helpers import ReturnDict

from agency.models import Project

from .tag import TagSerializer


class ProjectSerializer(ModelSerializer):
    tags = SerializerMethodField()

    def get_tags(self, obj: Project) -> ReturnDict:
        selected_tags = obj.tags.all()
        return TagSerializer(selected_tags, many=True).data

    class Meta:
        model = Project
        fields: list[str] = [
            "preview_image",
            "title",
            "descritpion",
            "customer",
            "place",
            "photographer",
            "video_url",
            "full_description",
            "type",
            "tags",
        ]
