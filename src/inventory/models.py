from django.db import models

from src.base.models import TimeStampedModel
from src.inventory.constants import MovementTypes


class ItemUnit(TimeStampedModel):
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.short_name

    class Meta:
        verbose_name = "Item Unit"
        verbose_name_plural = "Item Units"


class ItemBrand(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Item Brand"
        verbose_name_plural = "Item Brands"


class ItemCategory(TimeStampedModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)

    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Item Category"
        verbose_name_plural = "Item Categories"


class Warehouse(TimeStampedModel):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255, blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Warehouse"
        verbose_name_plural = "Warehouses"


class Item(TimeStampedModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True, blank=True, null=True)

    category = models.ForeignKey(
        ItemCategory, on_delete=models.SET_NULL, null=True, related_name="items"
    )
    brand = models.ForeignKey(ItemBrand, on_delete=models.SET_NULL, null=True, blank=True)
    unit = models.ForeignKey(ItemUnit, on_delete=models.PROTECT)

    selling_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stock_alert_qty = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Item Setup"


class StockLedger(TimeStampedModel):
    direction = models.SmallIntegerField(choices=((1, "IN"), (-1, "OUT")))
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name="stock_ledgers")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name="stock_ledgers")

    movement_type = models.CharField(max_length=20, choices=MovementTypes.choices())

    quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    purchase = models.ForeignKey(
        "purchase.Purchase",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="stock_entries",
    )
    sale = models.ForeignKey(
        "sales.Sales", on_delete=models.PROTECT, null=True, blank=True, related_name="stock_entries"
    )

    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["item"]),
            models.Index(fields=["warehouse"]),
            models.Index(fields=["movement_type"]),
            models.Index(fields=["purchase"]),
            models.Index(fields=["sale"]),
        ]

    def __str__(self):
        return f"{self.item} | {self.movement_type}"
