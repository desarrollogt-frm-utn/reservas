import os

from django.db import models
from django.template.defaultfilters import slugify

class Nivel(models.Model):
    #atributos
    nombre = models.TextField()
    
    cuerpo = models.ForeignKey(
        'Cuerpo',
        verbose_name='Cuerpo',
    )  