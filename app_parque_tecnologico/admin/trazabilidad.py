# coding=utf-8

from django.contrib import admin

from ..models import Trazabilidad


@admin.register(Trazabilidad)
class TrazabilidadAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de Trazabilidad en la interfaz de administración.
    """
    list_display = (
        '_recurso',
        'fecha_inicio',
        'fecha_fin',
        'seccion',
        'usuario'
    )

    def _recurso(self, obj):
        """
        Obtiene el Recurso asociado a la instancia.
        """
        return str(obj.recurso)
    _recurso.short_description = 'Recurso'
