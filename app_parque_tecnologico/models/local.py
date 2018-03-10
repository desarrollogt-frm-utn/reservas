# coding=utf-8

from django.db import models
from app_reservas.models import Nivel


class Local(models.Model):
    # Atributos
    nro_local = models.PositiveIntegerField()

    # Relaciones
    nivel = models.ForeignKey(Nivel)

    # Representación del objeto
    def __str__(self):
        return '{0!s}'.format(self.nro_local)

    # Información de la clase
    class Meta:
        app_label = 'app_parque_tecnologico'
        verbose_name = 'Local'
        verbose_name_plural = 'Locales'