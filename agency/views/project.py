from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from agency.models import Project
from agency.serializers.project import ProjectOneSerializer, ProjectSerializer


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.filter(published=True)
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectSerializer

        if self.action == "retrieve":
            return ProjectOneSerializer

        return ProjectSerializer
