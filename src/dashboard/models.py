from django.db import models


class TenantResource(models.Model):
    name = models.CharField(max_length=200)
    data = models.TextField(blank=True)

    class Meta:
        verbose_name = "Tenant Resource"
        verbose_name_plural = "Tenant Resources"

    def __str__(self):
        return f"{self.name} ({self.tenant.schema_name})"
