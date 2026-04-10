from django.urls import path
from tenants.admin_site import public_admin_site

urlpatterns = [
    path("admin/", public_admin_site.urls),
]
