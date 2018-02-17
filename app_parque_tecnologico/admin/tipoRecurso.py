# coding=utf-8

from django.contrib import admin

from ..models import TipoRecurso


@admin.register(TipoRecurso)
class TipoRecursoAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de TipoRecurso en la interfaz de administración.
    """
    list_display = (
        'nombre',
        'identificacion',
    )
