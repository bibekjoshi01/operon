from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import AdminDateWidget
from django.db import models

from .models import Purchase, PurchaseAdditionalCharge, PurchaseItem, PurchasePaymentDetail


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1
    fields = ("item", "quantity", "rate", "tax_rate", "discount_rate")

    formfield_overrides = {
        models.DecimalField: {"widget": forms.NumberInput(attrs={"style": "width:100px;"})}
    }


class PurchasePaymentInline(admin.TabularInline):
    model = PurchasePaymentDetail
    extra = 1
    fields = ("payment_mode", "amount")


class PurchaseAdditionalChargeInline(admin.TabularInline):
    model = PurchaseAdditionalCharge
    extra = 1
    fields = ("charge_type", "amount", "remarks")


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
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
                    "pay_type",
                    "bill_no",
                    "bill_date",
                    "supplier",
                    "warehouse",
                    "notes",
                ),
            },
        ),
    )

    formfield_overrides = {
        models.CharField: {"widget": forms.TextInput(attrs={"style": "width:200px;"})},
        models.IntegerField: {"widget": forms.NumberInput(attrs={"style": "width:200px;"})},
        models.DateField: {"widget": AdminDateWidget(attrs={"style": "width:180px;"})},
        models.TextField: {
            "widget": forms.Textarea(attrs={"rows": 3, "style": "width:100%; max-width:100%;"})
        },
        models.ForeignKey: {"widget": forms.Select(attrs={"style": "width:380px;"})},
    }

    def save_model(self, request, obj, form, change):
        if not change:
            form.cleaned_data.get("items", None)
            super().save_model(request, obj, form, change)
        else:
            super().save_model(request, obj, form, change)
