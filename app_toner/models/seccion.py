import os

from django.db import models
from django.template.defaultfilters import slugify

class Seccion(models.Model):
    #atributos
    nombre = models.TextField()

    area = models.ForeignKey(
        'Area',
        verbose_name='Area',
    )
    