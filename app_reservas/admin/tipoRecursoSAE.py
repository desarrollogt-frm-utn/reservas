# coding=utf-8

from django.contrib import admin

from ..models import TipoRecursoSAE


@admin.register(TipoRecursoSAE)
class TipoRecursoSAEAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de TipoRecursoSAE en la interfaz de administración.
    """
    list_display = (
        'nombre',
        'nombre_plural',
        'slug',
        'is_visible_navbar',
    )

    list_filter = (
        'is_visible_navbar',
    )
