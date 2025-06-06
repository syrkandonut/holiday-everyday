"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView, TemplateView

from .collectstatic import STATICFILES

urlpatterns = (
    [
        path("api/admin/", admin.site.urls),
        path("admin/", RedirectView.as_view(url="/api/admin/", permanent=True)),
        path("admin", RedirectView.as_view(url="/api/admin/", permanent=True)),
        path("api/", include("agency.urls")),
        path("api", RedirectView.as_view(url="/api/", permanent=True)),
        path(
            "api/projects", RedirectView.as_view(url="/api/projects/", permanent=True)
        ),
        path("api/media", RedirectView.as_view(url="/api/media/", permanent=True)),
        path("api/tags", RedirectView.as_view(url="api/tags/", permanent=True)),
        path("ckeditor5/", include("django_ckeditor_5.urls")),
    ]
    + STATICFILES
    + [
        re_path(r"^", TemplateView.as_view(template_name="index.html"), name="index"),
    ]
)
