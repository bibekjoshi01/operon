from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect


def home(request):
    tenant = getattr(request, 'tenant', None)
    if tenant:
        return HttpResponse(f"Dashboard for tenant: {tenant.name}")
    # No tenant found for this hostname — treat as vendor/public site and redirect to admin
    return redirect('/admin/')
