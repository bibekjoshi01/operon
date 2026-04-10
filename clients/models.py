from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=200)
    subdomain = models.SlugField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.subdomain})"
