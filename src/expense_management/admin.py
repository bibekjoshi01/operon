from django.contrib import admin
from django.db.models import Sum
from django.utils.html import format_html

from src.base.admin import BaseAdmin

from .models import Expense, ExpenseAttachment, ExpenseCategory


# INLINE: ATTACHMENTS
# -------------------------
class ExpenseAttachmentInline(admin.TabularInline):
    model = ExpenseAttachment
    extra = 0
    fields = ("file", "name")


# CATEGORY ADMIN
# -------------------------
@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(BaseAdmin):
    list_display = (
        "serial_number",
        "name",
        "total_expense",
        "created_at",
        "edit_action",
    )
    search_fields = ("name",)
    ordering = ("name",)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(total_amount=Sum("expenses__amount"))

    fieldsets = (
        (
            "Basic Info",
            {"fields": (("name", "is_active"), ("description",))},
        ),
    )

    def total_expense(self, obj):
        return format_html(
            "<strong style='color:#10B981;'>₹ {}</strong>",
            obj.total_amount or 0,
        )

    total_expense.short_description = "Total Expense"


# EXPENSE ADMIN
# -------------------------
@admin.register(Expense)
class ExpenseAdmin(BaseAdmin):
    inlines = [ExpenseAttachmentInline]

    list_display = (
        "serial_number",
        "title",
        "category",
        "amount_display",
        "expense_date",
        "attachment_count",
        "created_at",
        "edit_action",
    )

    list_filter = ("category", "expense_date", "created_at")
    search_fields = ("title", "description", "category__name")
    ordering = ("-expense_date",)

    fieldsets = (
        (
            "Expense Info",
            {
                "fields": (
                    ("title", "category"),
                    ("amount", "expense_date"),
                    "description",
                )
            },
        ),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)

        if db_field.name == "amount":
            formfield.widget.attrs.update({"style": "width: 300px;"})

        return formfield

    def get_queryset(self, request):
        return (
            super().get_queryset(request).select_related("category").prefetch_related("attachments")
        )

    def amount_display(self, obj):
        return format_html(
            "<strong style='color:#EF4444;'>₹ {}</strong>",
            obj.amount,
        )

    amount_display.short_description = "Amount"

    def attachment_count(self, obj):
        count = obj.attachments.count()
        if count:
            return format_html(
                "<span style='background:#111827;color:white;padding:3px 8px;border-radius:10px;font-size:12px;'>"
                "{} files</span>",
                count,
            )
        return "-"

    attachment_count.short_description = "Attachments"
