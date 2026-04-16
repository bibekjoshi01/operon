from django.contrib import admin

from src.base.admin import BaseAdmin

from .models import AdditionalChargeType, PaymentMethod


@admin.register(AdditionalChargeType)
class AdditionalChargeTypeAdmin(BaseAdmin):
    actions = None

    list_display = (
        "name",
        "created_at",
        "is_active",
        "edit_action",
    )

    search_fields = ("name",)
    fieldsets = (("Basic Info", {"fields": ("name", "is_active")}),)
    list_filter = ("created_at",)


@admin.register(PaymentMethod)
class PaymentMethodAdmin(BaseAdmin):
    actions = None

    list_display = (
        "name",
        "created_at",
        "is_active",
        "edit_action",
    )

    search_fields = ("name",)
    fieldsets = (("Basic Info", {"fields": ("name", "is_active")}),)
    list_filter = ("created_at",)
