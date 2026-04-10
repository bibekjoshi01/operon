from django.contrib import admin


class TenantAdminSite(admin.AdminSite):
    def each_context(self, request):
        ctx = super().each_context(request)
        tenant = getattr(request, 'tenant', None)
        if tenant:
            ctx['site_header'] = f"{tenant.name} Admin"
            ctx['site_title'] = f"{tenant.name} Admin"
        return ctx


tenant_admin_site = TenantAdminSite(name='tenant_admin')
