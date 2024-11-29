import os

from django.db import models
from django.template.defaultfilters import slugify

class Impresora(models.Model):
    #atributos
    idImpresora = models.TextField()

    ip = models.TextField()

    observacion = models.TextField()

    idPC = models.TextField()

    conexion = models.TextField()

    marca = models.ForeignKey(
        'TipoImpresora',
        verbose_name='Marca',
    )

    seccion = models.ForeignKey(
        'Seccion',
        verbose_name='Seccion',
    )

    local = models.ForeignKey(
        'Local',
        verbose_name='Local',
    )