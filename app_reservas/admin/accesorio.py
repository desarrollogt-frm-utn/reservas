# coding=utf-8

from django.contrib import admin

from ..models import Accesorio


@admin.register(Accesorio)
class AccesorioAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de Accesorio en la interfaz de administración.
    """
    list_display = (
        '_identificador',
        '_tipo',
        'activo',
    )

    list_filter = (
        'tipo',
    )

    def _identificador(self, obj):
        """
        Obtiene el identificador de la instancia.
        """
        return obj.get_nombre_corto()
    _identificador.short_description = 'Identificador'
    _identificador.admin_order_field = 'identificador'

    def _tipo(self, obj):
        """
        Obtiene el tipo asociado a la instancia.
        """
        return obj.tipo
    _tipo.short_description = 'Tipo'
    _tipo.admin_order_field = 'tipo__nombre'
