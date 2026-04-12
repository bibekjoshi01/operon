from django.contrib import admin
from django.contrib.auth.models import Group

admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        perms = super().get_model_perms(request)
        return perms

    def has_module_permission(self, request):
        return True

    def get_queryset(self, request):
        return super().get_queryset(request)


Group._meta.verbose_name = "Role"
Group._meta.verbose_name_plural = "Roles"
