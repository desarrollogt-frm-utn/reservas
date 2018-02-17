# coding=utf-8

from django.db import models


class Proveedor(models.Model):
    # Atributos
    nombre = models.CharField(max_length=50)
    telefono = models.PositiveIntegerField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # Representación del objeto
    def __str__(self):
        return '{0!s}'.format(self.nombre)

    # Información de la clase
    class Meta:
        app_label = 'app_parque_tecnologico'
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedor'
