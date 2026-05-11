from django.db import transaction
from django.utils import timezone

from src.order_management.constants import OrderTypes

from .models import Order


class OrderService:
    @staticmethod
    @transaction.atomic
    def finalize_order(order):
        sub_total = 0

        for item in order.items.all():
            line_total = item.quantity * item.rate

            item.gross_amount = line_total
            item.net_amount = line_total
            item.save(update_fields=["gross_amount", "net_amount"])

            sub_total += line_total

        total_charges = sum(ch.amount for ch in order.additional_charges.all())

        order.sub_total = sub_total
        order.grand_total = sub_total + total_charges

        order.save(update_fields=["sub_total", "grand_total"])

        return order

    def generate_order_no(type: str):
        # generate invoice number
        last = (
            Order.objects.select_for_update()
            .exclude(order_no__isnull=True)
            .order_by("-order_no")
            .first()
        )

        order_no = (last.order_no + 1) if last else 1
        prefix = "ORD" if type == OrderTypes.ORDER else "OR"
        order_no_full = f"{prefix}-{timezone.now().year}-{order_no:06d}"

        return order_no, order_no_full
