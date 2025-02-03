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

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, re_path, path
from django.views.generic.base import TemplateView, RedirectView

from config import settings

urlpatterns = (
    [
        path("api/admin/", admin.site.urls),
        path("admin/", RedirectView.as_view(url='/api/admin/', permanent=True)),
        path("api/", include("agency.urls")),
    ]
    + static(settings.IMAGE_URL, document_root=settings.IMAGE_ROOT)
    + static(settings.IMAGE_THUMB_URL, document_root=settings.IMAGE_THUMB_ROOT)
    + static(settings.STATIC_ASSETS_URL, document_root=settings.STATIC_ASSETS_ROOT)
    + static(settings.STATIC_IMAGES_URL, document_root=settings.STATIC_IMAGES_ROOT)
    + [
        re_path(r"^", TemplateView.as_view(template_name="index.html"), name="index"),
    ]
)
