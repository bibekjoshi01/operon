from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

from src.base.admin import BaseAdmin
from src.purchase.constants import PurchaseTypes
from src.purchase.service import PurchaseService

from .models import (
    PurchaseAdditionalCharge,
    PurchaseInvoice,
    PurchaseItem,
    PurchasePaymentDetail,
    PurchaseReturn,
)


class PurchaseItemInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        if any(self.errors):
            return

        has_items = False

        for form in self.forms:
            if not form.cleaned_data:
                continue

            if form.cleaned_data.get("DELETE", False):
                continue

            # ignore empty inline rows
            if form.cleaned_data.get("item"):
                has_items = True

        if not has_items:
            raise ValidationError("At least one sales item is required.")


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1
    formset = PurchaseItemInlineFormSet

    fields = ("item", "quantity", "rate", "tax_rate", "discount_rate")


class PurchasePaymentInline(admin.TabularInline):
    model = PurchasePaymentDetail
    extra = 1
    fields = ("payment_mode", "amount", "remarks")


class PurchaseAdditionalChargeInline(admin.TabularInline):
    model = PurchaseAdditionalCharge
    extra = 1
    fields = ("charge_type", "amount", "remarks")


@admin.register(PurchaseInvoice)
class PurchaseAdmin(BaseAdmin):
    inlines = [PurchaseItemInline, PurchasePaymentInline, PurchaseAdditionalChargeInline]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(purchase_type=PurchaseTypes.PURCHASE)

    def has_change_permission(self, request, obj=...):
        return False

    list_display = (
        "serial_number",
        "pay_type",
        "bill_no",
        "bill_date",
        "purchase_no_full",
        "supplier",
        "warehouse",
        "total_tax",
        "total_discount",
        "sub_total",
        "grand_total",
    )

    list_filter = (
        "pay_type",
        "supplier",
        "purchase_no_full",
        "created_at",
    )

    search_fields = ("supplier", "purchase_no_full", "bill_no")

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
            obj.purchase_type = PurchaseTypes.PURCHASE
            obj.purchase_no, obj.purchase_no_full = PurchaseService.generate_purchase_no(
                type=PurchaseTypes.PURCHASE
            )
            obj.sub_total = 0
            obj.grand_total = 0

        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        PurchaseService.finalize_purchase(form.instance)


@admin.register(PurchaseReturn)
class PurchaseReturnAdmin(BaseAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(purchase_type=PurchaseTypes.RETURN)
