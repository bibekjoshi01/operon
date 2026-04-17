from django.contrib import admin
from django.urls import include, path

print("TENANT URLS LOADED")

urlpatterns = [
    path("purchase/", include("src.purchase.urls")),
    path("", admin.site.urls),
]
