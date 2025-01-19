from django.core.exceptions import ObjectDoesNotExist
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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:
            project_review = instance.review
            data["review"] = ReviewSerializer(project_review).data
        except ObjectDoesNotExist:
            pass

        project_images = instance.images.all()
        if project_images:
            data["images"] = ImageSerializer(project_images, many=True).data
        return data

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
            # "images",
            # "review",
        ]
