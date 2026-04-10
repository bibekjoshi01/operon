from django.db import models
from tenants.models import Tenant


class TenantResource(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='resources')
    name = models.CharField(max_length=200)
    data = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.tenant.subdomain})"
