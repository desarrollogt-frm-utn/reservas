# coding=utf-8

from django.contrib import admin

from ..models import AlumnoComision


@admin.register(AlumnoComision)
class AlumnoComision(admin.ModelAdmin):
    """
    Especificación de la representación de Area en la interfaz de administración.
    """
    list_display = (
        'legajo',
        'comision',
    )