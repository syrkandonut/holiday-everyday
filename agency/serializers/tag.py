from rest_framework.serializers import ModelSerializer

from agency.models import Tag


class ProjectTagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id"]


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]
