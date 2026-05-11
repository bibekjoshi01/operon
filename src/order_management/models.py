from django.core.validators import MinValueValidator
from django.db import models

from src.base.models import TimeStampedModel
from src.order_management.constants import ItemUnits, OrderTypes


class Item(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    unit = models.CharField(max_length=20, choices=ItemUnits.choices(), default=ItemUnits.PCS.value)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Item Setup"


class Customer(TimeStampedModel):
    full_name = models.CharField(max_length=255)

    phone_no = models.CharField(max_length=20, blank=True)
    phone_no_alt = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.full_name}"

    class Meta:
        ordering = ("full_name",)


class OrderStatus(TimeStampedModel):
    """Dynamic order workflow status model."""

    name = models.CharField(max_length=100, unique=True)

    slug = models.SlugField(max_length=120, unique=True)
    color = models.CharField(
        max_length=20, default="#6B7280", help_text="Hex color code for frontend badge display"
    )
    sequence = models.PositiveIntegerField(
        default=0, help_text="Controls ordering of statuses in pipeline"
    )
    is_default = models.BooleanField(default=False, help_text="Default status when creating order")
    is_terminal = models.BooleanField(
        default=False, help_text="Final stage status like Delivered or Cancelled"
    )

    class Meta:
        ordering = ["sequence", "id"]
        verbose_name = "Order Status"
        verbose_name_plural = "Order Statuses"

    def __str__(self):
        return self.name


class Order(TimeStampedModel):
    order_type = models.CharField(choices=OrderTypes.choices(), max_length=20)

    order_no = models.PositiveBigIntegerField()
    order_no_full = models.CharField(max_length=50, unique=True)
    bill_no = models.CharField(max_length=50, blank=True)
    bill_date = models.DateField(null=True, blank=True)

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="customer_orders")

    discount_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    tax_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    sub_total = models.DecimalField(
        max_digits=12, decimal_places=2, editable=False, validators=[MinValueValidator(0)]
    )
    grand_total = models.DecimalField(
        max_digits=12, decimal_places=2, editable=False, validators=[MinValueValidator(0)]
    )

    description = models.CharField(max_length=500, blank=True)
    status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT, related_name="orders")
    notes = models.TextField(blank=True)
    is_urgent = models.BooleanField(default=False, help_text="Is this a priority order?")
    deadline_date = models.DateField(null=True, blank=True)

    ref_order = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self) -> str:
        return self.order_no_full

    class Meta:
        ordering = ["-created_at", "-id"]
        indexes = [
            models.Index(fields=["customer"]),
            models.Index(fields=["order_no_full"]),
        ]
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

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

    ref_order_item = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.item.name} x {self.quantity}"

    class Meta:
        ordering = ["id"]
        indexes = [
            models.Index(fields=["order"]),
            models.Index(fields=["item"]),
        ]
        constraints = [
            models.UniqueConstraint(fields=["order", "item"], name="unique_item_per_order")
        ]
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"


class PaymentMethod(TimeStampedModel):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Payment Method"
        verbose_name_plural = "Payment Methods"


class OrderPaymentDetail(TimeStampedModel):
    payment_mode = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="payment_details")
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    remarks = models.CharField(max_length=50, blank=True)

    def __str__(self) -> str:
        return str(self.amount)

    class Meta:
        indexes = [models.Index(fields=["order"])]
        verbose_name = "Payment Detail"
        verbose_name_plural = "Payment Details"


class OrderAdditionalCharge(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="additional_charges")
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    remarks = models.CharField(max_length=50, blank=True)

    class Meta:
        indexes = [models.Index(fields=["order"])]
        verbose_name = "Additional Charge"
        verbose_name_plural = "Additional Charges"

    def __str__(self) -> str:
        return self.charge_type.name


class OrderInvoice(Order):
    class Meta:
        proxy = True
        verbose_name = "Order"
        verbose_name_plural = "Orders"
