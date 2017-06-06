# coding=utf-8

from django.contrib import admin

from ..models import Comision, Horario, DocenteComision


class HorarioInline(admin.TabularInline):
    model = Horario


class DocenteComisionInline(admin.TabularInline):
    model = DocenteComision


class HorarioCursadoAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de Area en la interfaz de administración.
    """
    list_display = (
        'comision',
        'anioacademico',
        'cuatrimestre',
        'materia',
    )

    list_filter = (
        'anioacademico',
        'materia',
    )



    inlines = [
        HorarioInline,
        DocenteComisionInline,

    ]

admin.site.register(Comision, HorarioCursadoAdmin)