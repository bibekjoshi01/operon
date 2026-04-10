from django.contrib import admin

from tenants.models import Tenant, Domain, User


class TenantAdmin(admin.ModelAdmin):
    list_display = ("name", "subdomain", "created")


class DomainAdmin(admin.ModelAdmin):
    list_display = ("domain", "tenant", "is_primary")


class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "is_active"]
    list_display_links = ["id", "email"]
    search_fields = ["email"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "email",
                    "password",
                ],
            },
        ),
        (
            "Administrative",
            {
                "fields": [
                    "tenants",
                    "last_login",
                    "is_active",
                    "is_verified",
                ],
            },
        ),
    ]


admin.site.register(Tenant, TenantAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(User, UserAdmin)
