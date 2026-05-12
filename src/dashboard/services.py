from datetime import date

from django.db.models import Count, Q, Sum
from django.utils.timezone import now

from src.expense_management.models import Expense
from src.order_management.models import Customer, OrderInvoice, OrderStatus


# -------------------------
# CORE FILTER FUNCTION
# -------------------------
def get_filtered_orders(range_filter="all"):
    today = now().date()
    qs = OrderInvoice.objects.all()

    if range_filter == "today":
        qs = qs.filter(created_at__date=today)

    elif range_filter == "month":
        qs = qs.filter(
            created_at__year=today.year,
            created_at__month=today.month,
        )

    elif range_filter == "year":
        qs = qs.filter(created_at__year=today.year)

    return qs


# -------------------------
# MAIN DASHBOARD METRICS
# -------------------------
def get_dashboard_metrics(range_filter="all"):
    today = date.today()
    orders = get_filtered_orders(range_filter)

    # -------------------------
    # ORDER COUNTS
    # -------------------------
    active_orders = orders.exclude(status__is_terminal=True).count()
    total_orders = orders.count()

    completed_today = orders.filter(
        status__is_terminal=True, status__slug="delivered", updated_at__date=today
    ).count()

    customer_count = Customer.objects.count()

    # -------------------------
    # FINANCIALS (IMPORTANT FIX)
    # -------------------------
    revenue = orders.aggregate(total=Sum("grand_total"))["total"] or 0

    paid = orders.aggregate(total=Sum("payment_details__amount"))["total"] or 0

    pending_payments = revenue - paid

    expenses = Expense.objects.aggregate(total=Sum("amount"))["total"] or 0

    net_profit = revenue - expenses

    return {
        # order stats
        "active_orders": active_orders,
        "completed_today": completed_today,
        "total_orders": total_orders,
        "customer_count": customer_count,
        # financials
        "revenue": revenue,
        "paid": paid,
        "pending_payments": pending_payments,
        "expenses": expenses,
        "net_profit": net_profit,
    }


# -------------------------
# STATUS DISTRIBUTION (for pie chart)
# -------------------------
def get_order_status_distribution(range_filter="all"):
    orders = get_filtered_orders(range_filter)

    return list(
        OrderStatus.objects.annotate(count=Count("orders", filter=Q(orders__in=orders)))
        .values("name", "color", "count")
        .order_by("sequence")
    )
