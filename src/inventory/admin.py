from django.contrib import admin

from src.base.admin import BaseAdmin

from .models import Item, ItemBrand, ItemCategory, ItemUnit, Warehouse


@admin.register(ItemUnit)
class ItemUnitAdmin(BaseAdmin):
    actions = None

    list_display = (
        "serial_number",
        "name",
        "short_name",
        "created_at",
        "is_active",
        "edit_action",
    )

    search_fields = ("name", "short_name")
    fieldsets = (("Unit Info", {"fields": ("name", "short_name", "is_active")}),)
    list_filter = ("created_at",)


@admin.register(ItemBrand)
class ItemBrandAdmin(BaseAdmin):
    actions = None

    list_display = (
        "serial_number",
        "name",
        "created_at",
        "is_active",
        "edit_action",
    )

    search_fields = ("name",)

    fieldsets = (("Brand Info", {"fields": ("name", "is_active")}),)

    list_filter = ("created_at",)


@admin.register(ItemCategory)
class ItemCategoryAdmin(BaseAdmin):
    actions = None

    list_display = (
        "serial_number",
        "name",
        "code",
        "parent",
        "created_at",
        "is_active",
        "edit_action",
    )

    search_fields = ("name", "code")
    list_filter = ("created_at", "parent")

    fieldsets = (
        (
            "Category Info",
            {
                "fields": (
                    "name",
                    "code",
                    "parent",
                    "is_active",
                )
            },
        ),
    )


@admin.register(Warehouse)
class WarehouseAdmin(BaseAdmin):
    actions = None

    list_display = (
        "serial_number",
        "name",
        "location",
        "is_default",
        "created_at",
        "is_active",
        "edit_action",
    )

    search_fields = ("name", "location")
    list_filter = ("is_default", "created_at")

    fieldsets = (("Warehouse Info", {"fields": ("name", "location", "is_default", "is_active")}),)


@admin.register(Item)
class ItemAdmin(BaseAdmin):
    actions = None

    list_display = (
        "serial_number",
        "name",
        "code",
        "category",
        "brand",
        "unit",
        "selling_price",
        "created_at",
        "is_active",
        "edit_action",
    )

    search_fields = ("name", "code")

    list_filter = (
        "category",
        "brand",
        "unit",
        "created_at",
    )

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "code", "category", "brand", "unit", "description", "is_active")},
        ),
        ("Pricing & Stock", {"fields": ("selling_price", "stock_alert_qty")}),
    )
