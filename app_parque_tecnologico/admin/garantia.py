# coding=utf-8

from django.contrib import admin

from ..models import Garantia


@admin.register(Garantia)
class GarantiaAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de Garantia en la interfaz de administración.
    """
    list_display = (
        'fecha_compra',
        'fecha_expiracion',
        'nro_factura'
    )
