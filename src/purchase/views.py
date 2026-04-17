from django.http import JsonResponse

from .models import Purchase, PurchaseItem, PurchaseTypes


def get_purchases_by_supplier(request):
    supplier_id = request.GET.get("supplier")

    purchases = Purchase.objects.filter(
        supplier_id=supplier_id, purchase_type=PurchaseTypes.PURCHASE
    ).values("id", "bill_no", "purchase_no_full")

    return JsonResponse(
        {
            "results": [
                {"id": p["id"], "text": f"{p['purchase_no_full']} ({p['bill_no']})"}
                for p in purchases
            ]
        }
    )


def get_purchase_items_by_purchase(request):
    purchase_id = request.GET.get("purchase")

    items = PurchaseItem.objects.filter(purchase_id=purchase_id).select_related("item")

    data = [
        {
            "item_id": i.item_id,
            "item_name": i.item.name,
            "quantity": float(i.quantity),
            "rate": float(i.rate),
            "tax_rate": float(i.tax_rate),
            "discount_rate": float(i.discount_rate),
            "gross_amount": float(i.gross_amount),
            "net_amount": float(i.net_amount),
        }
        for i in items
    ]

    return JsonResponse({"results": data})
