from django.http import HttpResponse
from django.shortcuts import redirect


def home(request):
    tenant = getattr(request, "tenant", None)
    if tenant:
        return HttpResponse(f"Dashboard for tenant: {tenant.name}")
    return redirect("/admin/")
