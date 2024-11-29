# coding=utf-8

from django.contrib import admin

from ..models import TipoToner


@admin.register(TipoToner)
class TipoToneraAdmin(admin.ModelAdmin):
    """
    Especificación de la representación del tipo de toner en la interfaz de administración.
    """
    list_display = (
        '_codigo',
        '_stockIdeal',
        '_entrada',
        '_salida',
    )