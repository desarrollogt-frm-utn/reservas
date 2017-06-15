# coding=utf-8

"""
Django settings for reservas project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import random
from django.core.urlresolvers import reverse_lazy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Establece la clave secreta a partir de la variable de entorno 'DJANGO_SECRET_KEY', o genera una
# clave aleatoria si ésta no se encuentra seteada.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY',
                            ''.join([random.SystemRandom()
                                     .choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
                                     for i in range(50)]))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Administradores del proyecto.
ADMINS = []
MANAGERS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djangobower',
    'app_facturacion',
    'app_reservas.apps.ReservasConfig',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'reservas.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'reservas.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Establece el prefijo para el proyecto Django, según la configuración
# del servidor web.
DJANGO_URL_PREFIX = os.environ.get('DJANGO_URL_PREFIX', '')
# Da formato al prefijo URL, para que sea de la forma '<prefijo>/'.
# 1. Quita las barras iniciales y finales, por si el prefijo cuenta con más de una.
DJANGO_URL_PREFIX = DJANGO_URL_PREFIX.strip('/')
# 2. Añade una única barra final, en caso de que el prefijo no haya quedado vacío luego de la
# operación anterior.
if DJANGO_URL_PREFIX:
    DJANGO_URL_PREFIX += '/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/' + DJANGO_URL_PREFIX + 'static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/' + DJANGO_URL_PREFIX + 'media/'

BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'components')

BOWER_INSTALLED_APPS = (
    'bootstrap-datepicker',
    'bootswatch-dist#flatly',
    'font-awesome',
    'fullcalendar-scheduler',
    'handsontable#0.31.2',
    'jquery#1.9.1',
    'pace',
    'qtip2',
    'slick-carousel',
    'bootstrap',
    'seiyria-bootstrap-slider',
    'eonasdan-bootstrap-datetimepicker',
)

# Token de Google Calendar, utilizado para consultar la información de eventos
# de los calendarios de Google Calendar.
GOOGLE_CALENDAR_TOKEN = os.environ.get('GOOGLE_CALENDAR_TOKEN', '')

BROKER_URL = os.environ.get('BROKER_URL', 'amqp://guest:guest@rabbit//')

LOGIN_URL = '/' + DJANGO_URL_PREFIX + 'cuentas/login/'

LOGIN_REDIRECT_URL = reverse_lazy('solicitud_listar')
