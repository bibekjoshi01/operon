from django.contrib import admin

from .services import (
    get_dashboard_metrics,
    get_order_status_distribution,
)


class CustomAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}

        metrics = get_dashboard_metrics()
        status_data = get_order_status_distribution()

        range_filter = request.GET.get("range", "all")

        extra_context.update(
            {
                **metrics,
                "status_data": status_data,
                "selected_range": range_filter,
            }
        )

        return super().index(request, extra_context)


admin.site.__class__ = CustomAdminSite
