from django.db import models
from clients.models import Client


class TenantResource(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='resources')
    name = models.CharField(max_length=200)
    data = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.client.subdomain})"
