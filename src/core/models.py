from django.db import models

from src.base.models import TimeStampedModel


class AdditionalChargeType(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class PaymentMethod(TimeStampedModel):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name
