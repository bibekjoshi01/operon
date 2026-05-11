from django.contrib import admin
from django.urls import path

print("TENANT URLS LOADED")

urlpatterns = [
    path("", admin.site.urls),
]
