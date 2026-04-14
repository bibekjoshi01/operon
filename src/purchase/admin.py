from django.contrib import admin

from .models import Purchase, PurchaseItem


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    inlines = [PurchaseItemInline]
    save_on_top = True

    list_display = (
        "bill_no",
        "supplier",
        "warehouse",
        "bill_date",
        "grand_total",
    )

    def save_model(self, request, obj, form, change):
        if not change:
            form.cleaned_data.get("items", None)
            super().save_model(request, obj, form, change)
        else:
            super().save_model(request, obj, form, change)
