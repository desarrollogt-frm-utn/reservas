from django.contrib import admin

# coding=utf-8

from django.contrib import admin

from .models import Usuario


@admin.register(Usuario)
class AreaAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de Usuario en la interfaz de administración.
    """
    list_display = (
        'email',
        'legajo',
        'first_name',
        'last_name',
    )
    list_filter = (
        'is_active',
    )
