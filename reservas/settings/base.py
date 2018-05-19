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
import datetime
import raven

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
TEST = False

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
    'app_parque_tecnologico',
    'app_reservas.apps.ReservasConfig',
    'app_usuarios',
    'rolepermissions',
    'constance',
    'constance.backends.database',
    'captcha',
    'raven.contrib.django.raven_compat',
    'django.contrib.postgres',
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



CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 600,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'es-la'

TIME_ZONE = 'America/Mendoza'

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


SITE_URL = os.environ.get('SITE_URL', 'http://localhost:8080/' + DJANGO_URL_PREFIX)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/' + DJANGO_URL_PREFIX + 'static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # default
    'app_usuarios.emailLogin.EmailLogin', # Email login
    'app_usuarios.glpiLogin.GlpiLogin'
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
    'bootstrap-datepicker#1.6.0',
    'bootswatch-dist#3.3.6-flatly',
    'font-awesome',
    'fullcalendar-scheduler',
    'handsontable#0.31.2',
    'jquery#1.9.1',
    'pace#1.0.2',
    'qtip2#2.2.1',
    'slick-carousel#1.6.0',
    'bootstrap'
)

# Token de Google Calendar, utilizado para consultar la información de eventos
# de los calendarios de Google Calendar.
GOOGLE_CALENDAR_TOKEN = os.environ.get('GOOGLE_CALENDAR_TOKEN', '')

BROKER_URL = os.environ.get('BROKER_URL', 'amqp://guest:guest@rabbit//')

LOGIN_URL = '/' + DJANGO_URL_PREFIX + 'cuentas/login/'

LOGIN_REDIRECT_URL = reverse_lazy('index')

ROLEPERMISSIONS_MODULE = 'app_reservas.roles'

GOOGLE_SECRET_JSON_FILE = os.path.join(BASE_DIR, 'Reservas-FRM-UTN.json')


CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_CONFIG = {
    'FECHA_INICIO_PRIMER_SEMESTRE': (datetime.datetime.now().date() , 'Fecha de inicio del primer semestre', datetime.date),
    'FECHA_FIN_PRIMER_SEMESTRE': (datetime.datetime.now().date() , 'Fecha de fin del primer semestre', datetime.date),
    'FECHA_INICIO_SEGUNDO_SEMESTRE': (datetime.datetime.now().date() , 'Fecha de inicio del segundo semestre', datetime.date),
    'FECHA_FIN_SEGUNDO_SEMESTRE': (datetime.datetime.now().date() , 'Fecha de fin del segundo semestre', datetime.date),
}

# Configuración de para el envío de emails
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.office365.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_USER', '')


CAPTCHA_OUTPUT_FORMAT = u'%(hidden_field)s<p>%(text_field)s</p><p>%(image)s</p>'

SENTRY_DNS = os.environ.get('SENTRY_DNS', '')
RAVEN_CONFIG = {
    'dsn': SENTRY_DNS,
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
}
GLPI_URL = os.environ.get('GLPI_URL', 'http://localhost/glpi')
GLPI_USER = os.environ.get('GLPI_USER', '')
GLPI_PASS = os.environ.get('GLPI_PASS', '')

WSDL_URL = os.environ.get('WSDL_URL','')
