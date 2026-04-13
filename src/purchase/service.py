from decimal import Decimal

from django.db import transaction

from src.inventory.constants import MovementTypes
from src.inventory.models import StockLedger

from .models import Purchase, PurchaseItem


class PurchaseService:
    @staticmethod
    @transaction.atomic
    def create_purchase(data, items_data, user):
        purchase = Purchase.objects.create(
            pay_type=data["pay_type"],
            purchase_no=data["purchase_no"],
            purchase_no_full=data["purchase_no_full"],
            supplier=data["supplier"],
            warehouse=data["warehouse"],
            bill_no=data["bill_no"],
            bill_date=data["bill_date"],
            total_discount=Decimal("0"),
            total_tax=Decimal("0"),
            sub_total=Decimal("0"),
            grand_total=Decimal("0"),
            notes=data.get("notes", ""),
        )

        sub_total = Decimal("0")
        total_tax = Decimal("0")
        total_discount = Decimal("0")

        for item in items_data:
            qty = item["quantity"]
            rate = item["rate"]

            gross = qty * rate

            tax_amount = item.get("tax_amount", Decimal("0"))
            discount_amount = item.get("discount_amount", Decimal("0"))

            net = gross + tax_amount - discount_amount

            PurchaseItem.objects.create(
                purchase=purchase,
                item=item["item"],
                quantity=qty,
                rate=rate,
                tax_rate=item.get("tax_rate", 0),
                tax_amount=tax_amount,
                discount_rate=item.get("discount_rate", 0),
                discount_amount=discount_amount,
                gross_amount=gross,
                net_amount=net,
            )

            StockLedger.objects.create(
                item=item["item"],
                warehouse=purchase.warehouse,
                movement_type=MovementTypes.PURCHASE,
                quantity=qty,
                purchase=purchase,
            )

            sub_total += gross
            total_tax += tax_amount
            total_discount += discount_amount

        purchase.sub_total = sub_total
        purchase.total_tax = total_tax
        purchase.total_discount = total_discount
        purchase.grand_total = sub_total + total_tax - total_discount
        purchase.save()

        return purchase
