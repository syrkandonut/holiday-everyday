from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from agency.models import Media
from agency.serializers.media import MediaSerializer


class MediaViewSet(ModelViewSet):
    queryset = Media.objects.all().order_by("-date")
    serializer_class = MediaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
