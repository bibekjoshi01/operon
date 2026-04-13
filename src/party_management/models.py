from django.db import models

from src.base.models import TimeStampedModel


class Supplier(TimeStampedModel):
    full_name = models.CharField(max_length=255)

    phone_no = models.CharField(max_length=20, blank=True)
    phone_no_alt = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    address = models.TextField(blank=True)
    pan_vat_no = models.CharField(max_length=50, blank=True)

    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.full_name}"

    class Meta:
        ordering = ("full_name",)


class Customer(TimeStampedModel):
    full_name = models.CharField(max_length=255)

    phone_no = models.CharField(max_length=20, blank=True)
    phone_no_alt = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    address = models.TextField(blank=True)
    pan_vat_no = models.CharField(max_length=50, blank=True)

    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.full_name}"

    class Meta:
        ordering = ("full_name",)
