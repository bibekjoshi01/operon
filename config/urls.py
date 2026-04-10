from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from website.views import home, register_tenant, registration_success

urlpatterns = [
    path("", home, name="home"),
    path("register/", register_tenant, name="register_tenant"),
    path("register/success/", registration_success, name="registration_success"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT or (settings.BASE_DIR / "static"))
