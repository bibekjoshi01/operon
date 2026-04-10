# Operon — Django SaaS starter

Quick scaffold for a modern Django SaaS app with subdomain-based tenants and per-client admin dashboards.

Quick start

1. Create a virtualenv and install requirements:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

-2. Configure environment variables (SECRET_KEY, DB_*), or edit `src/config/settings/dev.py`.

3. Add local hosts entries for subdomains (for testing):

```
# /etc/hosts (requires sudo)
127.0.0.1    tenant1.localhost
127.0.0.1    tenant2.localhost
```

4. Run migrations and start the dev server:

```bash
python manage.py migrate
python manage.py runserver
```

5. Create tenants easily:

```bash
# Create tenant and a superuser (optional)
python manage.py create_tenant --name "Tenant One" --subdomain tenant1 --create-superuser --username admin --email admin@example.com --password secret
```

6. Access tenant dashboard or admin:

- Dashboard: http://tenant1.localhost:8000/
- Admin: http://tenant1.localhost:8000/admin/

Postgres setup (optional — use if you want a Postgres-backed dev DB):

1. Install Postgres (macOS Homebrew example):

```bash
brew install postgresql
brew services start postgresql
```

2. Create DB user and database (adjust `DB_USER`/`DB_PASSWORD`):

```bash
createuser -s operon_user || true
psql -c "ALTER USER operon_user WITH PASSWORD 'secret';"
createdb -O operon_user operon_db || true
```

3. Edit the `.env` file at the project root and set `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`.

4. Install Postgres Python driver and helpers (already listed in `requirements.txt`):

```bash
pip install -r requirements.txt
```

5. Run migrations against Postgres:

```bash
python manage.py migrate
```

6. Create tenants and users as before:

```bash
python manage.py create_tenant --name "Tenant One" --subdomain tenant1 --create-superuser --username admin --email admin@example.com
```

Notes:
- The dev settings will use Postgres when `DB_HOST` is present in `.env`. Otherwise it keeps using SQLite for convenience.
- For production-grade multi-tenancy, follow `docs/multitenant_integration.md` to migrate to `django-tenants` and use Postgres schemas.

Files created
- `manage.py`, `src/config/` (settings, urls, wsgi/asgi)
- `src/clients/` (tenant model + admin + `create_tenant` command)
- `src/saas/` (middleware), `src/dashboard/` (per-tenant dashboard)
- plus package inits and small app configs.
