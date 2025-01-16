from django.contrib import admin

from .models import Feedback, Image, Media, Project, Review, Tag

admin.site.register(
    (
        Tag,
        Project,
        Review,
        Feedback,
        Media,
        Image,
    )
)
