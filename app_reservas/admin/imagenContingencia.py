# coding=utf-8

from django.contrib import admin

from ..models import ImagenContingencia


@admin.register(ImagenContingencia)
class ImagenContingenciaAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de ImagenContingencia en la interfaz de administración.
    """
    list_display = (
        'id',
        'descripcion',
        'activo',
    )

    list_filter = (
        'activo',
    )


