from datetime import date

from django.db.models import Count, Q, Sum
from django.utils.timezone import now

from src.expense_management.models import Expense
from src.order_management.models import Customer, OrderInvoice, OrderStatus


# CORE FILTER FUNCTION
# -------------------------
def get_filtered_orders(range_filter):
    today = now().date()
    orders = OrderInvoice.objects.all()
    expense = Expense.objects.all()

    if range_filter == "today":
        orders = orders.filter(created_at__date=today)
        expense = expense.filter(created_at__date=today)

    elif range_filter == "month":
        orders = orders.filter(
            created_at__year=today.year,
            created_at__month=today.month,
        )
        expense = expense.filter(
            created_at__year=today.year,
            created_at__month=today.month,
        )

    elif range_filter == "year":
        orders = orders.filter(created_at__year=today.year)
        expense = expense.filter(created_at__year=today.year)

    return orders, expense


# MAIN DASHBOARD METRICS
# -------------------------
def get_dashboard_metrics(range_filter):
    today = date.today()
    orders, expense = get_filtered_orders(range_filter)

    # ORDER COUNTS
    # -------------------------
    active_orders = orders.exclude(status__is_terminal=True).count()
    total_orders = orders.count()

    completed_today = OrderInvoice.objects.filter(
        status__slug="delivered", updated_at__date=today
    ).count()

    customer_count = Customer.objects.count()

    # FINANCIALS (IMPORTANT FIX)
    # -------------------------
    revenue = (
        orders.exclude(status__slug="cancelled").aggregate(total=Sum("grand_total"))["total"] or 0
    )
    paid = (
        orders.exclude(status__slug="cancelled").aggregate(total=Sum("payment_details__amount"))[
            "total"
        ]
        or 0
    )
    pending_payments = revenue - paid
    expenses = expense.aggregate(total=Sum("amount"))["total"] or 0

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


# STATUS DISTRIBUTION (for pie chart)
# -------------------------
def get_order_status_distribution(range_filter):
    orders, _ = get_filtered_orders(range_filter)

    return list(
        OrderStatus.objects.annotate(count=Count("orders", filter=Q(orders__in=orders)))
        .values("name", "color", "count")
        .order_by("sequence")
    )
