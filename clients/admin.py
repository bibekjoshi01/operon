from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'subdomain', 'is_active', 'created')
    search_fields = ('name', 'subdomain')
