from django.contrib import admin
from .models import TenantResource


class TenantScopedAdmin(admin.ModelAdmin):
    list_display = ('name', 'client')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        tenant = getattr(request, 'tenant', None)
        if tenant:
            return qs.filter(client=tenant)
        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # restrict client choices to the current tenant when in tenant context
        if db_field.name == 'client':
            tenant = getattr(request, 'tenant', None)
            if tenant:
                kwargs['queryset'] = tenant.__class__.objects.filter(pk=tenant.pk)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(TenantResource, TenantScopedAdmin)
