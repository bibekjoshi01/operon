from django.contrib import admin

from src.base.admin import BaseAdmin

from .constants import SaleTypes
from .models import SalesAdditionalCharge, SalesInvoice, SalesItem, SalesPaymentDetail, SalesReturn


class SalesItemInline(admin.TabularInline):
    model = SalesItem
    extra = 1
    fields = ("item", "quantity", "rate", "tax_rate", "discount_rate")


class SalesPaymentInline(admin.TabularInline):
    model = SalesPaymentDetail
    extra = 1
    fields = ("payment_mode", "amount", "remarks")


class SalesAdditionalChargeInline(admin.TabularInline):
    model = SalesAdditionalCharge
    extra = 1
    fields = ("charge_type", "amount", "remarks")


@admin.register(SalesInvoice)
class SalesAdmin(BaseAdmin):
    inlines = [SalesItemInline, SalesPaymentInline, SalesAdditionalChargeInline]
    save_on_top = True

    def get_queryset(self, request):
        return super().get_queryset(request).filter(sale_type=SaleTypes.SALE)

    list_display = (
        "sale_no_full",
        "customer",
        "grand_total",
    )

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    ("pay_type", "customer"),
                    "notes",
                ),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            form.cleaned_data.get("items", None)
            super().save_model(request, obj, form, change)
        else:
            super().save_model(request, obj, form, change)


@admin.register(SalesReturn)
class SaleReturnAdmin(BaseAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(sale_type=SaleTypes.RETURN)
