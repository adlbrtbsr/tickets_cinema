from .base import *

SECRET_KEY = "django-insecure-97ry^t44ifoffuhtom)j*6dy_(da2@wj9512z!ptv)4@dmko2e"

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": "db.",
        "PORT": "5432",
    }
}
