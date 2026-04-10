from django.contrib import admin
from .models import TenantResource


@admin.register(TenantResource)
class TenantResourceAdmin(admin.ModelAdmin):
    list_display = ("name", "tenant")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        tenant = getattr(request, "tenant", None)
        if tenant:
            return qs.filter(tenant=tenant)
        return qs.none()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "tenant":
            tenant = getattr(request, "tenant", None)
            if tenant:
                kwargs["queryset"] = tenant.__class__.objects.filter(pk=tenant.pk)
            else:
                kwargs["queryset"] = tenant.__class__.objects.none()  # type: ignore
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
