# coding=utf-8

from django.db import models


class Garantia(models.Model):
    # Atributos
    fecha_compra = models.DateField()
    fecha_expiracion = models.DateField()
    nro_factura = models.PositiveIntegerField()
    valor = models.DecimalField(max_digits=14, decimal_places=2)

    # Información de la clase
    class Meta:
        app_label = 'app_parque_tecnologico'
        verbose_name = 'Garantia'
        verbose_name_plural = 'Garantias'
