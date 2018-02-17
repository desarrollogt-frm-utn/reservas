# coding=utf-8

from django.db import models
from app_usuarios.models import Usuario


class Trazabilidad(models.Model):
    # Atributos
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    # Relaciones
    seccion = models.ForeignKey('Seccion')
    usuario = models.OneToOneField(Usuario)
    local = models.ForeignKey('Local')
    recurso = models.ForeignKey('Recurso', related_name='trazabilidades')

    # Representación del objeto

    # Información de la clase
    class Meta:
        app_label = 'app_parque_tecnologico'
        verbose_name = 'Trazabilidad'
        verbose_name_plural = 'Trazabilidades'
