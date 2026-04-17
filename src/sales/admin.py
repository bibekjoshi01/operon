from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

from src.base.admin import BaseAdmin
from src.sales.service import SaleService

from .constants import SaleTypes
from .models import SalesAdditionalCharge, SalesInvoice, SalesItem, SalesPaymentDetail, SalesReturn


class SalesItemInlineFormSet(BaseInlineFormSet):
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


class SalesItemInline(admin.TabularInline):
    model = SalesItem
    extra = 1
    formset = SalesItemInlineFormSet

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

    def get_queryset(self, request):
        return super().get_queryset(request).filter(sale_type=SaleTypes.SALE)

    list_display = (
        "serial_number",
        "pay_type",
        "sale_no_full",
        "customer",
        "total_tax",
        "total_discount",
        "sub_total",
        "grand_total",
    )

    list_filter = (
        "pay_type",
        "customer",
        "sale_no_full",
        "created_at",
    )

    search_fields = (
        "customer",
        "sale_no_full",
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
            obj.sale_type = SaleTypes.SALE
            obj.sale_no, obj.sale_no_full = SaleService.generate_sale_no(type=SaleTypes.SALE)
            obj.sub_total = 0
            obj.grand_total = 0

        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        SaleService.finalize_sale(form.instance)


@admin.register(SalesReturn)
class SaleReturnAdmin(BaseAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(sale_type=SaleTypes.RETURN)
