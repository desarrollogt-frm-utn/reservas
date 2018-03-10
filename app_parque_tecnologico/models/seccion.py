# coding=utf-8

from django.db import models
from app_reservas.models import Area


class Seccion(models.Model):
    # Atributos
    nombre = models.CharField(max_length=50)
    interno = models.PositiveIntegerField()
    descripcion = models.TextField(
        verbose_name='Descripciones',
        blank=True,
        null=True
    )

    # Relaciones
    area = models.ForeignKey(Area)

    # Representación del objeto
    def __str__(self):
        return '{0!s}'.format(self.nombre)

    # Información de la clase
    class Meta:
        app_label = 'app_parque_tecnologico'
        verbose_name = 'Sección'
        verbose_name_plural = 'Secciones'
