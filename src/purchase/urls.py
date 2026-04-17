from django.urls import path

from .views import get_purchase_items_by_purchase, get_purchases_by_supplier

urlpatterns = [
    path("purchase-by-supplier/", get_purchases_by_supplier, name="ajax-purchases"),
    path("purchase-items-by-purchase/", get_purchase_items_by_purchase),
]
