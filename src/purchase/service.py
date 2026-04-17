from django.db import transaction
from django.utils import timezone

from src.purchase.constants import PurchaseTypes

from .models import Purchase


class PurchaseService:
    @staticmethod
    @transaction.atomic
    def finalize_purchase(purchase):
        sub_total = 0

        for item in purchase.items.all():
            line_total = item.quantity * item.rate

            item.gross_amount = line_total
            item.net_amount = line_total
            item.save(update_fields=["gross_amount", "net_amount"])

            sub_total += line_total

        total_charges = sum(ch.amount for ch in purchase.additional_charges.all())

        purchase.sub_total = sub_total
        purchase.grand_total = sub_total + total_charges

        purchase.save(update_fields=["sub_total", "grand_total"])

        return purchase

    def generate_purchase_no(type: str):
        # generate invoice number
        last = (
            Purchase.objects.select_for_update()
            .exclude(purchase_no__isnull=True)
            .order_by("-purchase_no")
            .first()
        )

        purchase_no = (last.purchase_no + 1) if last else 1
        prefix = "PU" if type == PurchaseTypes.PURCHASE else "PR"
        purchase_no_full = f"{prefix}-{timezone.now().year}-{purchase_no:06d}"

        return purchase_no, purchase_no_full
