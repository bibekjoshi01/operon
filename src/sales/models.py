from django.core.validators import MinValueValidator
from django.db import models

from src.base.models import TimeStampedModel
from src.core.models import AdditionalChargeType, PaymentMethod
from src.inventory.models import Item
from src.party_management.models import Customer

from .constants import PayTypes, SaleTypes


class Sales(TimeStampedModel):
    pay_type = models.CharField(choices=PayTypes.choices(), max_length=20)
    sale_type = models.CharField(choices=SaleTypes.choices(), max_length=20)
    sale_no = models.PositiveBigIntegerField()
    sale_no_full = models.CharField(max_length=20, unique=True)

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="sales")

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

    ref_sale = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.sale_no_full

    class Meta:
        ordering = ["-created_at", "-id"]
        indexes = [
            models.Index(fields=["customer"]),
            models.Index(fields=["sale_no_full"]),
        ]
        verbose_name = "Sale"
        verbose_name_plural = "Sales"


class SalesItem(TimeStampedModel):
    sale = models.ForeignKey(Sales, on_delete=models.CASCADE, related_name="items")

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
        max_digits=12,
        decimal_places=2,
        default=0,
        editable=False,
        validators=[MinValueValidator(0)],
    )
    net_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        editable=False,
        validators=[MinValueValidator(0)],
    )

    ref_sale_item = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.item.name} x {self.quantity}"

    class Meta:
        ordering = ["id"]
        indexes = [
            models.Index(fields=["sale"]),
            models.Index(fields=["item"]),
        ]
        constraints = [
            models.UniqueConstraint(fields=["sale", "item"], name="unique_item_per_sale")
        ]
        verbose_name = "Sales Item"
        verbose_name_plural = "Sales Items"


class SalesPaymentDetail(TimeStampedModel):
    sale = models.ForeignKey(Sales, on_delete=models.PROTECT, related_name="payment_details")
    payment_mode = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    remarks = models.CharField(max_length=50, blank=True)

    def __str__(self) -> str:
        return self.payment_mode.name

    class Meta:
        indexes = [
            models.Index(fields=["sale"]),
            models.Index(fields=["payment_mode"]),
        ]
        verbose_name = "Payment Detail"
        verbose_name_plural = "Payment Details"


class SalesAdditionalCharge(TimeStampedModel):
    charge_type = models.ForeignKey(AdditionalChargeType, on_delete=models.PROTECT)
    sale = models.ForeignKey(Sales, on_delete=models.PROTECT, related_name="additional_charges")
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    remarks = models.CharField(max_length=50, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["sale"]),
            models.Index(fields=["charge_type"]),
        ]
        verbose_name = "Additional Charge"
        verbose_name_plural = "Additional Charges"

    def __str__(self) -> str:
        return self.charge_type.name


class SalesInvoice(Sales):
    class Meta:
        proxy = True
        verbose_name = "Sales"
        verbose_name_plural = "Sales"


class SalesReturn(Sales):
    class Meta:
        proxy = True
        verbose_name = "Sale Return"
        verbose_name_plural = "Sale Returns"
