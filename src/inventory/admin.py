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
        "edit_action",
    )

    search_fields = ("name", "short_name")
    fieldsets = (("Unit Info", {"fields": ("name", "short_name")}),)
    list_filter = ("created_at",)

    def has_delete_permission(self, request, obj=...):
        return False


@admin.register(ItemBrand)
class ItemBrandAdmin(BaseAdmin):
    actions = None

    list_display = (
        "serial_number",
        "name",
        "created_at",
        "edit_action",
    )

    search_fields = ("name",)

    fieldsets = (("Brand Info", {"fields": ("name",)}),)

    list_filter = ("created_at",)

    def has_delete_permission(self, request, obj=...):
        return False


@admin.register(ItemCategory)
class ItemCategoryAdmin(BaseAdmin):
    actions = None

    list_display = (
        "serial_number",
        "name",
        "code",
        "parent",
        "created_at",
        "edit_action",
    )

    search_fields = ("name", "code")
    list_filter = ("created_at", "parent")

    fieldsets = (("Category Info", {"fields": ("name", "code", "parent")}),)

    def has_delete_permission(self, request, obj=...):
        return False


@admin.register(Warehouse)
class WarehouseAdmin(BaseAdmin):
    actions = None

    list_display = (
        "serial_number",
        "name",
        "location",
        "is_default",
        "created_at",
        "edit_action",
    )

    search_fields = ("name", "location")
    list_filter = ("is_default", "created_at")

    fieldsets = (("Warehouse Info", {"fields": ("name", "location", "is_default")}),)


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
        "stock_alert_qty",
        "created_at",
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
        ("Basic Info", {"fields": ("name", "code", "category", "brand", "unit", "description")}),
        ("Pricing & Stock", {"fields": ("selling_price", "stock_alert_qty")}),
    )
