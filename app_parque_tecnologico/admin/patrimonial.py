# coding=utf-8

from django.contrib import admin

from ..models import Patrimonial


@admin.register(Patrimonial)
class PatrimonialAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de Patrimonial en la interfaz de administración.
    """
    list_display = (
        'id_patrimonial',
        'nro_expediente',
        'responsable',
    )
