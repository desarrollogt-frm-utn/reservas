# coding=utf-8

from django.contrib import admin

from ..models import Modificacion


@admin.register(Modificacion)
class ModificacionAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de Modificacion en la interfaz de administración.
    """
    list_display = (
        '_componente',
        'fecha',
    )

    list_filter = (
        'autor',
    )

    def _componente(self, obj):
        """
        Obtiene el Componente asociado a la instancia.
        """
        return str(obj.componente)
    _componente.short_description = 'Componente'
