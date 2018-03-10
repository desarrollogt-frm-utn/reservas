# coding=utf-8

from django.contrib import admin

from ..models import TipoComponente


@admin.register(TipoComponente)
class TipoComponenteAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de TipoComponente en la interfaz de administración.
    """
    list_display = (
        'nombre',
    )
