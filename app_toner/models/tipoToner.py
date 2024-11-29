import os

from django.db import models
from django.template.defaultfilters import slugify

class TipoToner(models.Model):
    #atributos
    codigo = models.TextField()

    stockIdeal = models.PositiveIntegerField()

    entrada = models.PositiveIntegerField()

    salida = models.PositiveIntegerField()

'''
    def get_stock_actual(self):
        stock_actual = entrada - salida
        return stock_actual
'''    