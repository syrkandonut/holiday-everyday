from django.urls import include, path
from rest_framework import routers

from agency import views

router = routers.DefaultRouter()

router.register("projects", views.ProjectViewSet)
router.register("tags", views.TagViewSet)
router.register("media", views.MediaViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
