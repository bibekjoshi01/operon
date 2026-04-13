from django.db import models

from src.base.models import TimeStampedModel


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
