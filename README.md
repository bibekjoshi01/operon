# Operon — Django SaaS starter

Quick scaffold for a modern Django SaaS app with subdomain-based tenants and per-client admin dashboards.

Quick start

1. Create a virtualenv and install requirements:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run migrations and create a superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```

3. Start the development server:

```bash
python manage.py runserver
```

4. Open the public admin at http://localhost:8000/admin and create a Tenant (or Client).

5. (Optional) Add a hosts entry for a tenant subdomain to test subdomain routing, e.g. `tenant1.localhost`.

6. Visit the tenant dashboard or admin at the tenant host.

python manage.py migrate_schemas --shared
python manage.py shell -c "from tenants.models import Tenant, Domain; t=Tenant.objects.create(schema_name='tenant2', name='Tenant2', subdomain='tenant2', is_active=True); Domain.objects.create(domain='tenant2.localhost', tenant=t, is_primary=False)"
python manage.py create_tenant_user tenant1 admin admin123 --is_staff --is_superuser
