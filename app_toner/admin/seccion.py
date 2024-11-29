# coding=utf-8

from django.contrib import admin

from ..models import Seccion


@admin.register(Seccion)
class SeccionAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de la seccion en la interfaz de administración.
    """
    list_display = (
        '_nombre',
    )