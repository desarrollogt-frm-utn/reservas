import os

from django.db import models
from django.template.defaultfilters import slugify

class CodigoAlternativo(models.Model):
    #atributos
    nombre = models.TextField()
    