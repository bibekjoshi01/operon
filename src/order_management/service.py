from django.db import transaction
from django.utils import timezone

from src.order_management.constants import OrderTypes

from .models import Order, OrderItem


class OrderService:
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
            Order.objects.select_for_update()
            .exclude(purchase_no__isnull=True)
            .order_by("-purchase_no")
            .first()
        )

        purchase_no = (last.purchase_no + 1) if last else 1
        prefix = "PU" if type == OrderTypes.PURCHASE else "PR"
        purchase_no_full = f"{prefix}-{timezone.now().year}-{purchase_no:06d}"

        return purchase_no, purchase_no_full


class OrderReturnService:
    @staticmethod
    def create_return(ref_purchase_id, supplier_id, notes, user):
        purchase = Order.objects.prefetch_related("items").get(id=ref_purchase_id)
        purchase_no, purchase_no_full = OrderService.generate_purchase_no(type=OrderTypes.RETURN)

        return_obj = Order.objects.create(
            purchase_type=OrderTypes.RETURN,
            supplier_id=supplier_id,
            ref_purchase_id=ref_purchase_id,
            purchase_no=purchase_no,
            purchase_no_full=purchase_no_full,
            warehouse=purchase.warehouse,
            bill_date=purchase.bill_date,
            bill_no=f"RET-{purchase.bill_no}",
            pay_type=purchase.pay_type,
            sub_total=purchase.sub_total,
            grand_total=purchase.grand_total,
            notes=notes,
            created_by=user,
        )

        for item in purchase.items.all():
            OrderItem.objects.create(
                purchase=return_obj,
                item=item.item,
                quantity=item.quantity,
                rate=item.rate,
                tax_rate=item.tax_rate,
                discount_rate=item.discount_rate,
                net_amount=item.net_amount,
                gross_amount=item.gross_amount,
                ref_purchase_item=item,
                created_by=user,
            )

        return return_obj
