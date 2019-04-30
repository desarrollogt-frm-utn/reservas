# coding=utf-8

from .production import *

# Archivo de configuración de desarrollo. Se basa en la configuración de
# producción, y permite determinar el estado del Debug mediante la variable de
# entorno 'DJANGO_DEBUG'.
DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
