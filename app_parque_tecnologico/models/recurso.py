# coding=utf-8

from django.db import models
from django.contrib.auth.models import User
from .garantia import Garantia
from .patrimonial import Patrimonial



class Recurso(models.Model):
    # Atributos
    nombre = models.CharField(
        verbose_name='Nombre',
        max_length=10,
        unique=True)
    fecha_alta = models.DateTimeField(
        verbose_name='Fecha de Alta',
    )
    observaciones = models.TextField(
        verbose_name='Observaciones',
        blank=True,
        null=True
    )
    nro_incidente = models.PositiveIntegerField(blank=True, null=True)
    # Relaciones
    patrimonial = models.OneToOneField(Patrimonial, blank=True, null=True)
    garantia = models.OneToOneField(Garantia, blank=True, null=True)
    autor = models.ForeignKey(User)
    tipo_recurso = models.ForeignKey('TipoRecurso')

    # Representación del objeto
    def __str__(self):
        return 'Recurso: {0!s}'.format(self.nombre)

    # Información de la clase
    class Meta:
        app_label = 'app_parque_tecnologico'
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'
