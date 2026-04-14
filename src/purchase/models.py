from django.core.validators import MinValueValidator
from django.db import models

from src.base.models import TimeStampedModel
from src.core.models import AdditionalChargeType, PaymentMethod
from src.inventory.models import Item, Warehouse
from src.party_management.models import Supplier

from .constants import PayTypes


class Purchase(TimeStampedModel):
    pay_type = models.CharField(choices=PayTypes.choices(), max_length=20)
    purchase_no = models.PositiveBigIntegerField()
    purchase_no_full = models.CharField(max_length=20, unique=True)

    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name="purchases")
    bill_no = models.CharField(max_length=50, unique=True)
    bill_date = models.DateField()

    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name="purchases")

    total_discount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    total_tax = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    sub_total = models.DecimalField(
        max_digits=12, decimal_places=2, editable=False, validators=[MinValueValidator(0)]
    )
    grand_total = models.DecimalField(
        max_digits=12, decimal_places=2, editable=False, validators=[MinValueValidator(0)]
    )

    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.bill_no

    class Meta:
        ordering = ["-bill_date", "-id"]
        indexes = [
            models.Index(fields=["bill_no"]),
            models.Index(fields=["supplier"]),
            models.Index(fields=["bill_date"]),
            models.Index(fields=["purchase_no_full"]),
        ]


class PurchaseItem(TimeStampedModel):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="items")

    item = models.ForeignKey(Item, on_delete=models.PROTECT)

    quantity = models.DecimalField(
        max_digits=12, decimal_places=2, default=1, validators=[MinValueValidator(1)]
    )
    rate = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )

    tax_rate = models.DecimalField(
        max_digits=6, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    tax_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )

    discount_rate = models.DecimalField(
        max_digits=6, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    discount_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )

    gross_amount = models.DecimalField(
        max_digits=12, decimal_places=2, editable=False, validators=[MinValueValidator(0)]
    )
    net_amount = models.DecimalField(
        max_digits=12, decimal_places=2, editable=False, validators=[MinValueValidator(0)]
    )

    def __str__(self) -> str:
        return f"{self.item.name} x {self.quantity}"

    class Meta:
        ordering = ["id"]
        indexes = [
            models.Index(fields=["purchase"]),
            models.Index(fields=["item"]),
        ]
        constraints = [
            models.UniqueConstraint(fields=["purchase", "item"], name="unique_item_per_purchase")
        ]
        verbose_name = "Purchase Item"
        verbose_name_plural = "Purchase Items"


class PurchasePaymentDetail(TimeStampedModel):
    purchase = models.ForeignKey(Purchase, on_delete=models.PROTECT, related_name="payment_details")
    payment_mode = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )

    def __str__(self) -> str:
        return self.payment_mode.name

    class Meta:
        indexes = [
            models.Index(fields=["purchase"]),
            models.Index(fields=["payment_mode"]),
        ]
        verbose_name = "Payment Detail"
        verbose_name_plural = "Payment Details"


class PurchaseAdditionalCharge(TimeStampedModel):
    charge_type = models.ForeignKey(AdditionalChargeType, on_delete=models.PROTECT)
    purchase = models.ForeignKey(
        Purchase, on_delete=models.PROTECT, related_name="additional_charges"
    )
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    remarks = models.CharField(max_length=50, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["purchase"]),
            models.Index(fields=["charge_type"]),
        ]
        verbose_name = "Additional Charge"
        verbose_name_plural = "Additional Charges"

    def __str__(self) -> str:
        return self.charge_type.name
