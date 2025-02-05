from django.contrib.admin import StackedInline, TabularInline

from agency.models import Image, Review


class ImageInLine(TabularInline):
    model = Image
    extra = 0
    fields = ["name"]

    min_num = 1


class ReviewInLine(StackedInline):
    model = Review

    min_num = 1
    max_num = 1
