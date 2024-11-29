# coding=utf-8

from django.contrib import admin

from ..models import TipoImpresora


@admin.register(TipoImpresora)
class TipoImpresoraAdmin(admin.ModelAdmin):
    """
    Especificación de la representación del tipo de impresora en la interfaz de administración.
    """
    list_display = (
        '_marcaModelo',
    )