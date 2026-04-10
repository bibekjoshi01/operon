from django.urls import path
from django.conf import settings
from website.views import home, register_tenant, registration_success
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", home, name="home"),
    path("register/", register_tenant, name="register_tenant"),
    path("register/success/", registration_success, name="registration_success"),
]

if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()
