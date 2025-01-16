from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from agency.models import Project
from agency.serializers.project import ProjectSerializer


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.BasePermission]
