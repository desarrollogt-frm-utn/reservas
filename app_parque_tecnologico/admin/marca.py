# coding=utf-8

from django.contrib import admin

from ..models import Marca


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de Marca en la interfaz de administración.
    """
    list_display = (
        'nombre',
    )
