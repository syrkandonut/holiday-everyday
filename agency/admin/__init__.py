from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User

from agency.models import Media, Project, Review, Tag

from .models import MediaAdmin, ProjectAdmin, ReviewAdmin, TagAdmin


class AgencySite(AdminSite):
    def get_app_list(self, request, format=None):
        app_dict = self._build_app_dict(request)

        app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())

        return app_list


admin.site = AgencySite()


admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Tag, TagAdmin)

# admin.site.register(Image)
