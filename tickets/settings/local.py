from .base import *

SECRET_KEY = "django-insecure-97ry^t44ifoffuhtom)j*6dy_(da2@wj9512z!ptv)4@dmko2e"

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
