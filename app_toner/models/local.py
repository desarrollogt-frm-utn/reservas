import os

from django.db import models
from django.template.defaultfilters import slugify

class Local(models.Model):
    #atributos
    nombre = models.TextField()
    
    nivel = models.ForeignKey(
        'Nivel',
        verbose_name='Nivel',
    )