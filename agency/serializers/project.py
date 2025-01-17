from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.utils.serializer_helpers import ReturnDict

from agency.models import Project

from .image import ImageSerializer
from .review import ReviewSerializer
from .tag import TagSerializer


class ProjectSerializer(ModelSerializer):
    tags = SerializerMethodField()

    def get_tags(self, obj: Project) -> ReturnDict:
        project_tags = obj.tags.all()
        return TagSerializer(project_tags, many=True).data

    images = SerializerMethodField()

    def get_images(self, obj: Project) -> ReturnDict:
        project_images = obj.images.all()
        return ImageSerializer(project_images, many=True).data

    review = SerializerMethodField()

    def get_review(self, obj: Project) -> ReturnDict:
        project_review = obj.review.all()
        return ReviewSerializer(project_review, many=True).data

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
            "images",
            "review",
        ]
