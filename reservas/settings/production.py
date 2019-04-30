# coding=utf-8

from .base import *
import os

DEBUG = True
ALLOWED_HOSTS = ['*']
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
TEST = True

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME',''),
        'USER': os.environ.get('DB_USERNAME',''),
        'PASSWORD': os.environ.get('DB_PASSWORD',''),
        'HOST': os.environ.get('DB_HOST',''),
        'PORT': 5432,
    }
}
