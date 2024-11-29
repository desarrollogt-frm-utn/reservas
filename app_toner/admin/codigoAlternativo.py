# coding=utf-8

from django.contrib import admin

from ..models import CodigoAlternativo


@admin.register(CodigoAlternativo)
class CodigoAlternativoAdmin(admin.ModelAdmin):
    """
    Especificación de la representación del codigo alternativo en la interfaz de administración.
    """
    list_display = (
        '_nombre',
    )