from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": config(
            "DATABASE_ENGINE", default="django.db.backends.postgresql_psycopg2"
        ),
        "NAME": config("DATABASE_NAME", default="feeder"),
        "USER": config("DATABASE_USER", default="feeder"),
        "PASSWORD": config("DATABASE_PASSWORD", default="feeder@sendcloud"),
        "HOST": config("DATABASE_HOST", default="db"),
        "PORT": config("DATABASE_PORT", default="5432"),
    }
}


# Used in local development
# CELERY_BROKER_URL = "redis://localhost:6379"
# CELERY_RESULT_BACKEND = "redis://localhost:6379"
