# coding=utf-8

from django.contrib import admin

from ..models import TipoAccesorio


@admin.register(TipoAccesorio)
class TipoAccesorioAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de TipoAccesorio en la interfaz de administración.
    """
    list_display = (
        'nombre',
        'descripcion',
    )
