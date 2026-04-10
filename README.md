# Operon — Django SaaS Starter

A modern Django SaaS application scaffold with multi-tenant support, subdomain-based tenant routing, and per-tenant admin dashboards.

## Prerequisites

- Python 3.9+
- PostgreSQL 12+
- pip or pipenv

## Environment Setup

### 1. Clone and Create Virtual Environment

```bash
git clone <repo-url>
cd operon
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

### 4. Initialize Database

Create the PostgreSQL database:

```bash
createdb operon_db
```

Run shared migrations (creates shared schema):

```bash
python manage.py migrate_schemas --shared
```

### 6. Start Development Server

```bash
python manage.py runserver
```

Access the application:

- **Public Portal**: http://localhost:8000

### Database Migrations

For shared schema:

```bash
python manage.py makemigrations
python manage.py migrate_schemas --shared
```
