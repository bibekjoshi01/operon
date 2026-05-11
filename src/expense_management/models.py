from django.db import models

from src.base.models import TimeStampedModel
from src.libs.storage import tenant_media_path


class ExpenseCategory(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Expense Category"
        verbose_name_plural = "Expense Categories"


class Expense(TimeStampedModel):
    category = models.ForeignKey(ExpenseCategory, on_delete=models.PROTECT, related_name="expenses")

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    expense_date = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.amount}"

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"


class ExpenseAttachment(TimeStampedModel):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name="attachments")

    file = models.FileField(upload_to=tenant_media_path)
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name
