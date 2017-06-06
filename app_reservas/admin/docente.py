# coding=utf-8

from django.contrib import admin

from ..models import Docente


@admin.register(Docente)
class Docente(admin.ModelAdmin):
    """
    Especificación de la representación de Area en la interfaz de administración.
    """
    list_display = (
        'legajo',
        'nombre',
        'correo',
    )