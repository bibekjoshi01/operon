from django.urls import path, include
from saas.admin import tenant_admin_site

urlpatterns = [
    path('admin/', tenant_admin_site.urls),
]
