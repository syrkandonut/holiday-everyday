from django.core.exceptions import ObjectDoesNotExist
from rest_framework.serializers import (
    ModelSerializer,
)

from agency.models import Image, Project, Review
from config.settings import IMAGE_URL, SERVER_NGINX_URI, STORAGE_IMAGE_PATH

from .image import ImageSerializer
from .review import ReviewSerializer
from .tag import ProjectTagSerializer


class ProjectCommonSerializer(ModelSerializer):
    def to_representation(self, instance: Project):
        data = super().to_representation(instance)

        data["preview_image"] = (
            str(SERVER_NGINX_URI)
            + IMAGE_URL
            + str(instance.preview_image).replace(STORAGE_IMAGE_PATH + "/", str())
        )

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

        return data


class ProjectOneSerializer(ProjectCommonSerializer):
    def to_representation(self, instance: Project):
        data = super().to_representation(instance)

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
            "description",
            "customer",
            "place",
            "photographer",
            "video_url",
            "full_description",
            "type",
            "tags",
            "published",
        ]


class ProjectSerializer(ProjectCommonSerializer):
    class Meta:
        model = Project
        fields: list[str] = [
            "id",
            "preview_image",
            "title",
            "customer",
            "type",
            "tags",
        ]
