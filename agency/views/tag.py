from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from agency.models import Tag
from agency.serializers.tag import TagSerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
