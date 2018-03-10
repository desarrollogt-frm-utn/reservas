# coding=utf-8

from django.contrib import admin

from ..models import Recurso


@admin.register(Recurso)
class RecursoAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de Recurso en la interfaz de administración.
    """
    list_display = (
        'nombre',
        'tipo_recurso',
    )

    list_filter = (
        'tipo_recurso',
    )
