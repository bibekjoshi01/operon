from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from clients.models import Client


class SubdomainTenantMiddleware(MiddlewareMixin):
    """Resolve tenant by subdomain and attach to the request as `request.tenant`.

    Simple implementation: looks for subdomain (first label) and finds active Client.
    For production, prefer tested libraries like `django-tenants`.
    """

    def process_request(self, request):
        host = request.get_host().split(':')[0]
        parts = host.split('.')
        tenant = None
        # Accept subdomains like `sub.example.com` and `sub.localhost` (two-part local hosts)
        if len(parts) >= 2:
            subdomain = parts[0]
            if subdomain and subdomain.lower() != 'www':
                try:
                    tenant = Client.objects.filter(subdomain=subdomain, is_active=True).first()
                except Exception:
                    tenant = None
        request.tenant = tenant
