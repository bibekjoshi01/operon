from django.db import transaction
from django.utils import timezone

from .models import Sales


class SaleService:
    @staticmethod
    @transaction.atomic
    def finalize_sale(sale):
        sub_total = 0

        for item in sale.items.all():
            line_total = item.quantity * item.rate

            item.gross_amount = line_total
            item.net_amount = line_total
            item.save(update_fields=["gross_amount", "net_amount"])

            sub_total += line_total

        total_charges = sum(ch.amount for ch in sale.additional_charges.all())

        sale.sub_total = sub_total
        sale.grand_total = sub_total + total_charges

        sale.save(
            update_fields=[
                "sale_no",
                "sale_no_full",
                "sub_total",
                "grand_total",
            ]
        )

        return sale

    def generate_sale_no():
        # generate invoice number
        last = (
            Sales.objects.select_for_update()
            .exclude(sale_no__isnull=True)
            .order_by("-sale_no")
            .first()
        )

        sale_no = (last.sale_no + 1) if last else 1
        sale_no_full = f"SL-{timezone.now().year}-{sale_no:06d}"

        return sale_no, sale_no_full
