from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


class Tenant(TenantMixin):
    name = models.CharField(max_length=200)
    subdomain = models.SlugField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    owner = models.CharField(max_length=150, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    # django-tenants: enable automatic schema creation when creating a tenant object
    auto_create_schema = True

    class Meta:
        verbose_name = "Tenant"
        verbose_name_plural = "Tenants"

    def __str__(self):
        return f"{self.name} ({self.subdomain})"


class Domain(DomainMixin):
    pass
