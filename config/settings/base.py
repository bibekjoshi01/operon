import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tenants",
    "saas",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "saas.middleware.SubdomainTenantMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DEFAULT_DB_CONFIG = {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": os.getenv("DB_NAME", "operon_db"),
    "USER": os.getenv("DB_USER", "postgres"),
    "PASSWORD": os.getenv("DB_PASSWORD", ""),
    "HOST": os.getenv("DB_HOST", "localhost"),
    "PORT": os.getenv("DB_PORT", "5432"),
}

DATABASES = {"default": DEFAULT_DB_CONFIG.copy()}

# Enable django-tenants by default; set `USE_TENANTS=False` in the environment to disable.
USE_TENANTS = os.getenv("USE_TENANTS", "True") == "True"
TENANT_BASE_DOMAIN = os.getenv("TENANT_BASE_DOMAIN", "localhost")
PUBLIC_SCHEMA_NAME = os.getenv("PUBLIC_SCHEMA_NAME", "public")

if USE_TENANTS:
    try:
        import django_tenants  # noqa: F401

        # Switch database engine to tenant-aware backend
        DATABASES["default"]["ENGINE"] = "django_tenants.postgresql_backend"

        # Define SHARED_APPS and TENANT_APPS per django-tenants expectations.
        SHARED_APPS = [
            "django_tenants",
            "tenants",
            # shared infrastructure; also duplicated in TENANT_APPS so tenant schemas get their own tables
            "django.contrib.contenttypes",
            "django.contrib.auth",
            "django.contrib.admin",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.staticfiles",
        ]

        TENANT_APPS = [
            # tenant-specific apps (each tenant gets isolated copies of these tables)
            "django.contrib.contenttypes",
            "django.contrib.auth",
            "django.contrib.sessions",
            "django.contrib.messages",
        ]

        # Rebuild INSTALLED_APPS in the order required by django-tenants, removing duplicates
        INSTALLED_APPS = list(SHARED_APPS) + [
            app for app in TENANT_APPS if app not in SHARED_APPS
        ]
        TENANT_MODEL = "tenants.Tenant"
        TENANT_DOMAIN_MODEL = "tenants.Domain"
        # Router for tenant-aware sync and tenant middleware insertion.
        DATABASE_ROUTERS = ("django_tenants.routers.TenantSyncRouter",)
        # Insert TenantMainMiddleware near the top (after SecurityMiddleware)
        MIDDLEWARE.insert(1, "django_tenants.middleware.main.TenantMainMiddleware")
    except Exception:
        # If django-tenants isn't installed the flag will have no effect.
        USE_TENANTS = False
        DATABASES["default"] = DEFAULT_DB_CONFIG

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"

# Force host-only cookies so auth/session cookies are not shared across subdomains.
SESSION_COOKIE_DOMAIN = None
CSRF_COOKIE_DOMAIN = None
