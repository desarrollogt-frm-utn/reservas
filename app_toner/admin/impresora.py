# coding=utf-8

from django.contrib import admin

from ..models import Impresora


@admin.register(Impresora)
class ImpresoraAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de la impresora en la interfaz de administración.
    """
    list_display = (
        '_idImpresora',
        '_ip',
        '_observacion',
        '_idPC',
        '_conexion',
    )