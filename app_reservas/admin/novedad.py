# coding=utf-8

from django.contrib import admin

from ..models import Novedad


@admin.register(Novedad)
class NovedadAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de la Novedad en la interfaz de administración.
    """
    list_display = (
        'slug',
    )
