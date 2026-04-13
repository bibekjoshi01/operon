from django.contrib import admin

from src.base.admin import BaseAdmin

from .models import Customer, Supplier


@admin.register(Supplier)
class SupplierAdmin(BaseAdmin):
    actions = None
    list_display = (
        "serial_number",
        "full_name",
        "phone_no",
        "email",
        "pan_vat_no",
        "credit_limit",
        "is_active",
        "created_at",
        "edit_action",
    )

    search_fields = (
        "full_name",
        "phone_no",
        "email",
        "pan_vat_no",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    fieldsets = (
        ("Basic Info", {"fields": ("full_name", "email", "phone_no", "phone_no_alt", "address")}),
        ("Financial", {"fields": ("pan_vat_no", "credit_limit")}),
    )


@admin.register(Customer)
class CustomerAdmin(BaseAdmin):
    actions = None
    list_display = (
        "serial_number",
        "full_name",
        "phone_no",
        "email",
        "pan_vat_no",
        "credit_limit",
        "is_active",
        "created_at",
        "edit_action",
    )

    search_fields = (
        "full_name",
        "phone_no",
        "email",
        "pan_vat_no",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    fieldsets = (
        ("Basic Info", {"fields": ("full_name", "email", "phone_no", "phone_no_alt", "address")}),
        ("Financial", {"fields": ("pan_vat_no", "credit_limit")}),
    )
