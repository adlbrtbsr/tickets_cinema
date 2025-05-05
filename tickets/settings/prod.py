import os
from .base import *

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = []

DATABASES = {
    #TODO set up prod database
}