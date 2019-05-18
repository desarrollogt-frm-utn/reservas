# coding=utf-8

from .base import *
import os

DEBUG = False
ALLOWED_HOSTS = ['*']
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
TEST = True

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}
