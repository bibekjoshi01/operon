from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    tenant = getattr(request, 'tenant', None)
    if tenant:
        return HttpResponse(f"Dashboard for tenant: {tenant.name}")
    return HttpResponse("Public landing or no tenant detected")
