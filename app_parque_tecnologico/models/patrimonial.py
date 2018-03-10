# coding=utf-8

from django.db import models


class Patrimonial(models.Model):
    # Atributos
    id_patrimonial = models.PositiveIntegerField()
    nro_expediente = models.CharField(max_length=12)
    responsable = models.CharField(max_length=25)

    # Representación del objeto
    def __str__(self):
        return '{0!s}'.format(self.id_patrimonial)

    # Información de la clase
    class Meta:
        app_label = 'app_parque_tecnologico'
        verbose_name = 'Patrimonial'
        verbose_name_plural = 'Patrimoniales'