from django.contrib.admin import StackedInline, TabularInline

from agency.models import Image, Review


class ImageInLine(TabularInline):
    model = Image
    extra = 0
    fields = ["name"]


class ReviewInLine(StackedInline):
    model = Review
