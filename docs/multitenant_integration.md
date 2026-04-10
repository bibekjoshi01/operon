Title: Integrating django-tenants (Postgres schema-based multi-tenancy)

This project uses a simple subdomain middleware for tenant resolution. For production-grade multi-tenancy (isolated schemas, migrations per-tenant), consider `django-tenants`.

High-level steps:

1. Use PostgreSQL as your database and install `django-tenants` and `psycopg2-binary`.

2. Change `DATABASES['default']` to point to Postgres in `src/config/settings/production.py`.

3. Follow `django-tenants` docs to:
   - add `django_tenants` to `INSTALLED_APPS` before `django.contrib.contenttypes` etc.
   - define a `Tenant` model (subclass `TenantMixin`) and a `Domain` model.
   - set `TENANT_MODEL` in settings.
   - configure `DATABASE_ROUTERS` and `SHARED_APPS` / `TENANT_APPS`.

4. Update middleware/routing to use `django_tenants.middleware.TenantMiddleware`.

Notes:
- `django-tenants` requires running migrations differently; read docs carefully.
- This scaffold keeps tenant resolution lightweight; migrate to `django-tenants` when you need schema isolation and strict data separation.
