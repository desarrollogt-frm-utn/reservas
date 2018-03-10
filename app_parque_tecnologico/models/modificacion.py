# coding=utf-8

from django.db import models
from django.contrib.auth.models import User


class Modificacion(models.Model):
    # Atributos
    fecha = models.DateTimeField()
    detalle = models.TextField(
        verbose_name='Detalles',
        blank=True,
        null=True
    )

    # Relaciones
    componente = models.ForeignKey('Componente')
    autor = models.OneToOneField(User)
    recurso = models.ForeignKey('Recurso', related_name='modificaciones')

    # Representación del objeto
    def __str__(self):
        return '{0!s}'.format(self.fecha)

    # Información de la clase
    class Meta:
        app_label = 'app_parque_tecnologico'
        verbose_name = 'Modificación'
        verbose_name_plural = 'Modificaciones'