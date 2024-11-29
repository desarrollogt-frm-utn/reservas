import os

from django.db import models
from django.template.defaultfilters import slugify

class Cuerpo(models.Model):
    #atributos
    nombre = models.TextField()
    