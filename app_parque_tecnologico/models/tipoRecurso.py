# coding=utf-8

from django.db import models


class TipoRecurso(models.Model):
    # Atributos
    nombre = models.CharField(max_length=50)
    identificacion = models.CharField(max_length=10)
    descripcion = models.TextField(
        verbose_name='Descripciones',
        blank=True,
        null=True
    )
    # Representación del objeto
    def __str__(self):
        return '{0!s}'.format(self.nombre)

    # Información de la clase
    class Meta:
        app_label = 'app_parque_tecnologico'
        verbose_name = 'Tipo de Recurso'
        verbose_name_plural = 'Tipos de Recursos'
