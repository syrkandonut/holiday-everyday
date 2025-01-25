from django.contrib.admin import TabularInline

from agency.models import Image, Review


class ImageInLine(TabularInline):
    model = Image
    extra = 0
    fields = ["name"]


class ReviewInLine(TabularInline):
    model = Review
