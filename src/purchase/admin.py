from django.contrib import admin

from src.base.admin import BaseAdmin

from .models import Purchase, PurchaseAdditionalCharge, PurchaseItem, PurchasePaymentDetail


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1
    fields = ("item", "quantity", "rate", "tax_rate", "discount_rate")


class PurchasePaymentInline(admin.TabularInline):
    model = PurchasePaymentDetail
    extra = 1
    fields = ("payment_mode", "amount")


class PurchaseAdditionalChargeInline(admin.TabularInline):
    model = PurchaseAdditionalCharge
    extra = 1
    fields = ("charge_type", "amount", "remarks")


@admin.register(Purchase)
class PurchaseAdmin(BaseAdmin):
    inlines = [PurchaseItemInline, PurchasePaymentInline, PurchaseAdditionalChargeInline]
    save_on_top = True

    list_display = (
        "bill_no",
        "supplier",
        "warehouse",
        "bill_date",
        "grand_total",
    )

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    ("pay_type", "supplier"),
                    ("bill_no", "bill_date"),
                    "warehouse",
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
