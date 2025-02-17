from django.contrib import admin


class TagAdmin(admin.ModelAdmin):
    fields = ["name"]

    def has_add_permission(self, request):
        return "project" not in request.path
