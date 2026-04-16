from django.db import models

from src.base.models import TimeStampedModel


class AdditionalChargeType(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Additional Charge Type"
        verbose_name_plural = "Additional Charge Types"


class PaymentMethod(TimeStampedModel):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Payment Method"
        verbose_name_plural = "Payment Methods"
