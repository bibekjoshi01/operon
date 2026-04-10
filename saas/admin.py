from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered


class TenantAdminSite(admin.AdminSite):
    site_header = "Vendor Admin"
    site_title = "Vendor Admin"

    def each_context(self, request):
        ctx = super().each_context(request)
        tenant = getattr(request, 'tenant', None)
        if tenant:
            ctx['site_header'] = f"{tenant.name} Admin"
            ctx['site_title'] = f"{tenant.name} Admin"
        else:
            ctx['site_header'] = self.site_header
            ctx['site_title'] = self.site_title
        return ctx


tenant_admin_site = TenantAdminSite(name='admin')


def _copy_default_registry_to_tenant_site():
    """Mirror all ModelAdmin registrations from the default admin.site to our tenant site."""
    admin.autodiscover()
    for model, model_admin in admin.site._registry.items():
        if model in tenant_admin_site._registry:
            continue
        try:
            tenant_admin_site.register(model, model_admin.__class__)
        except AlreadyRegistered:
            pass


_copy_default_registry_to_tenant_site()
