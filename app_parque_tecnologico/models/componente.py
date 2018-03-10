# coding=utf-8

from django.db import models
from .garantia import Garantia


class Componente(models.Model):
    # Atributos
    capacidad = models.CharField(max_length=10)
    modelo = models.CharField(max_length=25)
    nro_serie = models.CharField(max_length=30)
    MAC = models.CharField(max_length=17)

    # Relaciones
    tipo_componente = models.ForeignKey('TipoComponente')
    marca = models.ForeignKey('Marca')
    proveedor = models.ForeignKey('Proveedor')
    garantia = models.OneToOneField(Garantia, null=True, blank=True)
    recurso = models.ForeignKey('Recurso', blank=True, null=True, related_name='componente')

    # Representación del objeto
    def __str__(self):
        return '{0!s}'.format(self.nro_serie)

    # Información de la clase
    class Meta:
        app_label = 'app_parque_tecnologico'
        verbose_name = 'Componente'
        verbose_name_plural = 'Componentes'