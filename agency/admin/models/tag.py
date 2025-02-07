from django.contrib import admin


class TagAdmin(admin.ModelAdmin):
    fields = ["name"]
