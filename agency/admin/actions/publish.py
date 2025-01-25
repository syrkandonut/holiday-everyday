from django.contrib import admin


@admin.action(description="Опубликовать проект")
def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
