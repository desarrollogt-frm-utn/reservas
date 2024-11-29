# coding=utf-8

from django.contrib import admin

from ..models import Local


@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de local en la interfaz de administración.
    """
    list_display = (
        '_nombre',
    )