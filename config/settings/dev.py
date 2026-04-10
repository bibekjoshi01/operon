from .base import *

DEBUG = True

# Development DB selection:
# If `DB_HOST` is set in the environment (see .env), use Postgres for development.
# Otherwise fall back to SQLite for quick local runs.
import os

if os.getenv('DB_HOST'):
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'NAME': os.getenv('DB_NAME', 'operon_db'),
			'USER': os.getenv('DB_USER', 'postgres'),
			'PASSWORD': os.getenv('DB_PASSWORD', ''),
			'HOST': os.getenv('DB_HOST', 'localhost'),
			'PORT': os.getenv('DB_PORT', '5432'),
		}
	}
else:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.sqlite3',
			'NAME': BASE_DIR / 'db.sqlite3',
		}
	}
