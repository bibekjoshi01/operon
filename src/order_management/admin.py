from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from django.utils.html import format_html

from src.base.admin import BaseAdmin
from src.order_management.constants import OrderTypes
from src.order_management.service import OrderService

from .models import (
    Customer,
    Item,
    OrderAdditionalCharge,
    OrderInvoice,
    OrderItem,
    OrderPaymentDetail,
    PaymentMethod,
)

admin.site.unregister(Group)
admin.site.unregister(User)


@admin.register(PaymentMethod)
class PaymentMethodAdmin(BaseAdmin):
    actions = None
    list_display = (
        "serial_number",
        "name",
        "created_at",
        "is_active",
        "edit_action",
    )

    fieldsets = (
        (
            "Basic Info",
            {"fields": (("name", "is_active"),)},
        ),
    )


@admin.register(Customer)
class CustomerAdmin(BaseAdmin):
    actions = None
    list_display = (
        "serial_number",
        "full_name",
        "phone_no",
        "email",
        "created_at",
        "is_active",
        "edit_action",
    )

    search_fields = ("full_name", "phone_no", "email")
    list_filter = ("is_active", "created_at")

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    ("full_name", "email"),
                    ("phone_no", "phone_no_alt"),
                    "address",
                    "is_active",
                )
            },
        ),
    )


@admin.register(Item)
class ItemAdmin(BaseAdmin):
    actions = None
    list_display = (
        "serial_number",
        "name",
        "unit",
        "created_at",
        "is_active",
        "edit_action",
    )

    search_fields = ("name",)
    list_filter = ("is_active", "created_at")

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    ("name", "unit"),
                    "is_active",
                )
            },
        ),
    )


class OrderItemInlineFormSet(BaseInlineFormSet):
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


class OrderItemInlineForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = "__all__"
        labels = {
            "tax_rate": "Tax Rate (%)",
            "discount_rate": "Discount Rate (%)",
            "rate": "Unit Price",
            "quantity": "Qty",
        }

        widgets = {
            "item": forms.Select(attrs={"style": "width: 220px;"}),
            "quantity": forms.NumberInput(attrs={"style": "width: 80px;"}),
            "rate": forms.NumberInput(attrs={"style": "width: 120px;"}),
            "tax_rate": forms.NumberInput(attrs={"style": "width: 100px;"}),
            "discount_rate": forms.NumberInput(attrs={"style": "width: 100px;"}),
        }


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    form = OrderItemInlineForm

    extra = 1
    formset = OrderItemInlineFormSet

    fields = (
        "item",
        "quantity",
        "rate",
        "tax_rate",
        "discount_rate",
    )


class OrderPaymentInline(admin.TabularInline):
    model = OrderPaymentDetail
    extra = 1
    fields = ("payment_mode", "amount", "remarks")


class OrderAdditionalChargeInline(admin.TabularInline):
    model = OrderAdditionalCharge
    extra = 1
    fields = ("amount", "remarks")


@admin.register(OrderInvoice)
class OrderAdmin(BaseAdmin):
    inlines = [OrderItemInline, OrderPaymentInline, OrderAdditionalChargeInline]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(order_type=OrderTypes.ORDER)

    def has_change_permission(self, request, obj=...):
        return False

    list_display = (
        "serial_number",
        "bill_info",
        "order_no_full",
        "customer",
        "tax_amount",
        "discount_amount",
        "sub_total",
        "grand_total",
        "created_info",
    )

    def created_info(self, obj):
        return format_html(
            "<strong>{}</strong><br><small>{}</small>", obj.created_by, obj.created_at.date()
        )

    list_filter = ("customer", "order_no_full", "created_at")
    search_fields = ("customer", "order_no_full", "bill_no")

    def bill_info(self, obj):
        return format_html("<strong>{}</strong><br><small>{}</small>", obj.bill_no, obj.bill_date)

    bill_info.short_description = "Bill Info"
    created_info.short_description = "Created Info"

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    ("customer"),
                    ("bill_no", "bill_date"),
                    ("description", "deadline_date"),
                    ("notes", "is_urgent"),
                ),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.order_type = OrderTypes.ORDER
            obj.order_no, obj.order_no_full = OrderService.generate_order_no(type=OrderTypes.ORDER)
            obj.sub_total = 0
            obj.grand_total = 0

        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        OrderService.finalize_order(form.instance)
