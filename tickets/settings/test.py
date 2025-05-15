from .base import *

SECRET_KEY = "testing-django-key"

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "test_db",
        "USER": "postgres",
        "PASSWORD": "test_pass",
        "HOST": "db_test.",
        "PORT": "5432",
    }
}
