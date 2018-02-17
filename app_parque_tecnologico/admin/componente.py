# coding=utf-8

from django.contrib import admin

from ..models import Componente


@admin.register(Componente)
class ComponenteAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de Componente en la interfaz de administración.
    """
    list_display = (
        'modelo',
        'capacidad',
        'MAC'
    )
