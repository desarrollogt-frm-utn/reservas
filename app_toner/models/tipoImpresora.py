import os

from django.db import models
from django.template.defaultfilters import slugify

class TipoImpresora(models.Model):
    #atributos
    marcaModelo = models.TextField()
    compatibilidad = models.ManyToManyField()

    