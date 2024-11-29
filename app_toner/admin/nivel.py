# coding=utf-8

from django.contrib import admin

from ..models import Nivel


@admin.register(Nivel)
class NivelAdmin(admin.ModelAdmin):
    """
    Especificación de la representación del nivel en la interfaz de administración.
    """
    list_display = (
        '_nombre',
    )