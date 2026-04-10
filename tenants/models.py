from django.db import models
from django.conf import settings

try:
    # Prefer django-tenants models when installed
    from django_tenants.models import TenantMixin, DomainMixin

    class Tenant(TenantMixin):
        # Business fields (merged from previous `clients.Client` model)
        name = models.CharField(max_length=200)
        subdomain = models.SlugField(max_length=100, unique=True)
        is_active = models.BooleanField(default=True)
        owner = models.CharField(max_length=150, blank=True)
        created = models.DateTimeField(auto_now_add=True)

        # django-tenants: enable automatic schema creation when creating a tenant object
        auto_create_schema = True

        class Meta:
            verbose_name = 'Tenant'
            verbose_name_plural = 'Tenants'

        def __str__(self):
            return f"{self.name} ({self.subdomain})"


    class Domain(DomainMixin):
        pass

except Exception:  # pragma: no cover - fallback when django-tenants isn't installed
    # Fallback models keep the project runnable but don't provide real schema isolation.
    class Tenant(models.Model):
        # Fallback non-schema tenant used when django-tenants isn't available.
        name = models.CharField(max_length=200)
        schema_name = models.SlugField(max_length=100, unique=True)
        subdomain = models.SlugField(max_length=100, unique=True)
        is_active = models.BooleanField(default=True)
        created = models.DateTimeField(auto_now_add=True)

        class Meta:
            verbose_name = 'Tenant'
            verbose_name_plural = 'Tenants'

        def __str__(self):
            return f"{self.name} ({self.subdomain})"


    class Domain(models.Model):
        domain = models.CharField(max_length=200)
        tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

        def __str__(self):
            return self.domain
