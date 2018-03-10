# coding=utf-8

from django.contrib import admin

from ..models import Local


@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de Local en la interfaz de administración.
    """
    list_display = (
        '_nivel',
        'nro_local',
    )

    list_filter = (
        'nivel',
    )

    def _nivel(self, obj):
        """
        Obtiene el nivel asociado a la instancia.
        """
        return str(obj.nivel)
    _nivel.short_description = 'Nivel'
    _nivel.admin_order_field = 'nivel_numero'
