from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.forms.models import BaseInlineFormSet
from django.utils import timezone
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


class ItemFilter(admin.SimpleListFilter):
    title = "Item"
    parameter_name = "item"

    def lookups(self, request, model_admin):
        return Item.objects.values_list("id", "name")

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(items__item_id=self.value()).distinct()  # related_name="items"
        return queryset


@admin.register(OrderInvoice)
class OrderAdmin(BaseAdmin):
    inlines = [OrderItemInline, OrderPaymentInline, OrderAdditionalChargeInline]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(order_type=OrderTypes.ORDER)

    list_display = (
        "serial_number",
        "bill_info",
        "display_customer",
        "grand_total",
        "paid_amount",
        "display_status",
        "is_urgent",
        "deadline_status",
        "created_date",
        "edit_action",
    )

    def created_date(self, obj):
        return format_html("<span>{}</span>", obj.created_at.date())

    list_filter = ("customer", "created_at", ItemFilter)
    search_fields = ("customer", "order_no_full", "bill_no")

    def bill_info(self, obj):
        return (
            format_html("<strong>{}</strong><br><small>{}</small>", obj.order_no_full, obj.bill_no)
            if obj.order_no_full
            else "N/A"
        )

    def display_customer(self, obj):
        return (
            format_html(
                "<strong>{}</strong><br><small>{}</small>",
                obj.customer.full_name,
                obj.customer.phone_no,
            )
            if obj.customer
            else "N/A"
        )

    def display_status(self, obj):
        if not obj.status:
            return "-"

        return format_html(
            """
            <span style="
                background-color: {};
                color: white;
                padding: 4px 10px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: 500;
                display: inline-block;
            ">
                {}
            </span>
            """,
            obj.status.color,
            obj.status.name,
        )

    display_customer.short_description = "Customer Info"
    display_status.short_description = "Status"
    bill_info.short_description = "Bill Info"
    created_date.short_description = "Order Date"

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    ("customer",),
                    ("status",),
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

    def deadline_status(self, obj):
        if not obj.deadline_date:
            return "-"

        today = timezone.localdate()
        diff = (obj.deadline_date - today).days

        date_str = obj.deadline_date.strftime("%Y-%m-%d")

        # Overdue
        if diff < 0:
            return format_html(
                "<span>{}</span><br>"
                "<span style='color:#EF4444;font-size:12px;font-weight:600;'>"
                "Overdue ({} days)</span>",
                date_str,
                abs(diff),
            )

        # Due today
        if diff == 0:
            return format_html(
                "<span>{}</span><br>"
                "<span style='color:#F59E0B;font-size:12px;font-weight:600;'>"
                "Due Today</span>",
                date_str,
            )

        # Upcoming
        return format_html(
            "<span>{}</span><br>"
            "<span style='color:#10B981;font-size:12px;font-weight:600;'>"
            "{} days remaining</span>",
            date_str,
            diff,
        )

    deadline_status.short_description = "Deadline Status"

    def paid_amount(self, obj):
        total_paid = obj.payment_details.aggregate(total=Sum("amount"))["total"] or 0

        grand_total = obj.grand_total or 0

        status = "PAID" if total_paid >= grand_total else "UNPAID"

        status_color = "#10B981" if status == "PAID" else "#EF4444"

        return format_html(
            "<strong style='color:#10B981;'>₹ {}</strong><br>"
            "<span style='color:{};font-size:12px;font-weight:600;'>{}</span>",
            total_paid,
            status_color,
            status,
        )

    paid_amount.short_description = "Paid Amount"
