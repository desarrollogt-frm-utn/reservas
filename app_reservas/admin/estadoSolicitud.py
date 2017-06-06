# coding=utf-8

from django.contrib import admin

from ..models import EstadoSolicitud


@admin.register(EstadoSolicitud)
class EstadoSolicitud(admin.ModelAdmin):
    """
    Especificación de la representación del Tipo de Solicitud en la interfaz de administración.
    """
    list_display = (
        'nombre',
        'descripcion',
    )