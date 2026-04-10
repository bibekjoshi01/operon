from django.contrib.admin import AdminSite
from .models import Tenant, Domain


class PublicAdminSite(AdminSite):
    site_header = "Vendor Admin"
    site_title = "SaaS Control Panel"


public_admin_site = PublicAdminSite(name="public_admin")

public_admin_site.register(Tenant)
public_admin_site.register(Domain)
