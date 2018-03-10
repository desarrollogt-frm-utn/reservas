# coding=utf-8

from django.contrib import admin

from ..models import Proveedor


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de Proveedor en la interfaz de administración.
    """
    list_display = (
        'nombre',
        'telefono',
        'email',
    )
