# coding=utf-8

from django.contrib import admin

from ..models import Plan


@admin.register(Plan)
class Plan(admin.ModelAdmin):
    """
    Especificación de la representación de Area en la interfaz de administración.
    """
    list_display = (
        'nombre',
        'descripcion',
    )