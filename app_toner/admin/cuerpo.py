# coding=utf-8

from django.contrib import admin

from ..models import Cuerpo


@admin.register(Cuerpo)
class CuerpoAdmin(admin.ModelAdmin):
    """
    Especificación de la representación del cuerpo en la interfaz de administración.
    """
    list_display = (
        '_nombre',
    )