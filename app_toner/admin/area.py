# coding=utf-8

from django.contrib import admin

from ..models import Area


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de Area en la interfaz de administración.
    """
    list_display = (
        '_nombre',
    )