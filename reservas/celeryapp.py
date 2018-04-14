# coding=utf-8

import os

from celery import Celery
from datetime import timedelta


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservas.settings.production')

from django.conf import settings  # noqa

app = Celery('reservas')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.CELERYBEAT_SCHEDULE = {
    'obtener_eventos_recursos': {
        'task': 'obtener_eventos_recursos',
        'schedule': timedelta(minutes=15)
    },
    'obtener_especialidades': {
        'task': 'obtener_especialidades',
        'schedule': timedelta(days=30)
    },
    'obtener_materias': {
        'task': 'obtener_materias',
        'schedule': timedelta(days=30)
    },
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
