from django.core.exceptions import ObjectDoesNotExist
from rest_framework.serializers import (
    ModelSerializer,
)

from agency.models import Image, Project, Review

from .image import ImageSerializer
from .review import ReviewSerializer
from .tag import ProjectTagSerializer


class ProjectSerializer(ModelSerializer):

    def to_representation(self, instance: Project):
        data = super().to_representation(instance)

        try:
            project_review = Review.objects.get(project=instance)
            serialized_review = ReviewSerializer(project_review).data
            data["review"] = serialized_review
        except ObjectDoesNotExist:
            ...

        project_tags = instance.tags.all()
        if project_tags:
            data["tags"] = [
                tag["id"] for tag in ProjectTagSerializer(project_tags, many=True).data
            ]

        project_images = Image.objects.filter(project=instance)
        if project_images:
            data["images"] = [
                image["name"]
                for image in ImageSerializer(project_images, many=True).data
            ]

        return data

    class Meta:
        model = Project
        fields: list[str] = [
            "id",
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
