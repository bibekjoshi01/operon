from django.contrib import admin, messages
from django.conf import settings
from django.core.management import call_command

from saas.admin import tenant_admin_site
from .models import Tenant, Domain


def _is_public_request(request) -> bool:
    """Return True when the current request is hitting the vendor/public schema."""
    public_schema = getattr(settings, "PUBLIC_SCHEMA_NAME", "public")
    tenant = getattr(request, "tenant", None)
    # No tenant resolved -> treat as public/vendor site
    if tenant is None:
        return True
    return getattr(tenant, "schema_name", None) == public_schema


@admin.register(Tenant, site=tenant_admin_site)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("name", "subdomain", "schema_name", "is_active", "created")
    search_fields = ("name", "subdomain", "schema_name")
    prepopulated_fields = {"schema_name": ("subdomain",)}

    # Only allow management from public/vendor admin
    def has_module_permission(self, request):
        return _is_public_request(request)

    def has_view_permission(self, request, obj=None):
        return _is_public_request(request)

    def has_add_permission(self, request):
        return _is_public_request(request)

    def has_change_permission(self, request, obj=None):
        return _is_public_request(request)

    def has_delete_permission(self, request, obj=None):
        return _is_public_request(request)

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        # Auto-fill schema_name from subdomain when missing (django-tenants requirement)
        if not getattr(obj, "schema_name", None):
            obj.schema_name = (obj.subdomain or "").replace("-", "_")
        super().save_model(request, obj, form, change)

        if is_new:
            # create domain mapping if not exists
            try:
                base_domain = getattr(settings, "TENANT_BASE_DOMAIN", "localhost")
                Domain.objects.get_or_create(
                    domain=f"{obj.subdomain}.{base_domain}", tenant=obj
                )
            except Exception:
                pass

            # If django-tenants is enabled, attempt to run tenant migrations
            if getattr(settings, "USE_TENANTS", False):
                try:
                    # TenantMixin.auto_create_schema will also create + sync schema on save;
                    # this explicit call ensures migrations run if auto_create_schema is False.
                    call_command(
                        "migrate_schemas",
                        schema_name=getattr(obj, "schema_name", None),
                        interactive=False,
                    )
                    messages.success(
                        request, f"Tenant schema created and migrated: {obj}"
                    )
                except Exception as exc:
                    messages.warning(
                        request, f"Tenant created but tenant migrations failed: {exc}"
                    )


@admin.register(Domain, site=tenant_admin_site)
class DomainAdmin(admin.ModelAdmin):
    list_display = (
        ("domain", "tenant", "is_primary")
        if hasattr(Domain, "is_primary")
        else ("domain", "tenant")
    )
    search_fields = ("domain",)

    # Only expose domains in public/vendor admin
    def has_module_permission(self, request):
        return _is_public_request(request)

    def has_view_permission(self, request, obj=None):
        return _is_public_request(request)

    def has_add_permission(self, request):
        return _is_public_request(request)

    def has_change_permission(self, request, obj=None):
        return _is_public_request(request)

    def has_delete_permission(self, request, obj=None):
        return _is_public_request(request)


# Also expose the models on Django's default admin site for convenience (e.g., shell_plus)
admin.site.register(Tenant, TenantAdmin)
admin.site.register(Domain, DomainAdmin)
