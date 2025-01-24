from django.contrib import admin


@admin.action(description="Перенести проект в архив")
def make_unpublished(modeladmin, request, queryset):
    queryset.update(published=False)
