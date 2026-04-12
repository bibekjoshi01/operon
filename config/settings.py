# ruff: noqa
import os
from pathlib import Path
from dotenv import load_dotenv
from .jazzmin_settings import *

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
APPS_DIR = BASE_DIR / "src"

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = ["*"]

SHARED_APPS = (
    "jazzmin",
    "django_ckeditor_5",
    "django_tenants",
    "tenants",
    "website",
)

TENANT_APPS = (
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.admin",
    "src.user",
)

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

MIDDLEWARE = [
    "django_tenants.middleware.TenantMainMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.tenant_urls"
PUBLIC_SCHEMA_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "website" / "templates", BASE_DIR / "templates"],
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

DATABASES = {
    "default": {
        "ENGINE": "django_tenants.postgresql_backend",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

TENANT_MODEL = "tenants.Tenant"
TENANT_DOMAIN_MODEL = "tenants.Domain"
DATABASE_ROUTERS = ("django_tenants.routers.TenantSyncRouter",)

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

SESSION_COOKIE_DOMAIN = None
CSRF_COOKIE_DOMAIN = None

# SECURITY
# ------------------------------------------------------------------------------
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# PASSWORDS
# ------------------------------------------------------------------------------
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# FIXTURES
# ------------------------------------------------------------------------------
FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# LOGGING
# ------------------------------------------------------------------------------

# Define the log directory
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

try:
    os.chmod(LOG_DIR, 0o775)
except PermissionError:
    pass


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": (
                "[{asctime}] {levelname} "
                "{name} | {filename}:{lineno} in {funcName}() | {message}"
            ),
            "style": "{",
        },
    },
    "handlers": {
        "security_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": str(LOG_DIR / "security_log"),
            "when": "midnight",  # rotate at midnight
            "interval": 1,  # every 1 day
            "backupCount": 7,  # keep last 7 days
            "formatter": "detailed",
            "level": "INFO",
            "encoding": "utf-8",
        },
        "server_error_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": str(LOG_DIR / "server_log"),  # base filename
            "when": "midnight",  # rotate at midnight
            "interval": 1,  # every 1 day
            "backupCount": 7,  # keep last 7 days
            "formatter": "detailed",
            "level": "INFO",
            "encoding": "utf-8",
        },
        "email_error_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": str(LOG_DIR / "email_log"),  # base filename
            "when": "midnight",  # rotate at midnight
            "interval": 1,  # every 1 day
            "backupCount": 7,  # keep last 7 days
            "formatter": "detailed",
            "level": "INFO",
            "encoding": "utf-8",
        },
    },
    "loggers": {
        # Django internal logs (Automatic)
        "django.security": {  # CSRF/auth/security warnings
            "handlers": ["security_file"],
            "level": "INFO",
            "propagate": False,
        },
        # Customer Manual logs
        "server_error": {
            "handlers": ["server_error_file"],
            "level": "INFO",
            "propagate": False,
        },
        "email_error": {
            "handlers": ["email_error_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


# STATIC
# ------------------------------------------------------------------------------
STATIC_ROOT = str(BASE_DIR / "staticfiles")
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
