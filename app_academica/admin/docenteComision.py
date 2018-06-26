# coding=utf-8

from django.contrib import admin

from ..models.docenteComision import DocenteComision


@admin.register(DocenteComision)
class DocenteComision(admin.ModelAdmin):
    """
    Especificación de la representación de Area en la interfaz de administración.
    """
    list_display = (
        'grado',
        '_comision',
        '_materia',
        'docente',
    )


    def _comision(self, obj):
        """
        Obtiene la comisión asociado a la instancia.
        """
        return obj.comision.get_nombre_corto()
    _comision.short_description = 'Comisión'

    def _materia(self, obj):
        """
        Obtiene la materia asociada a la instancia
        """
        return obj.comision.materia.get_nombre_corto()
    _materia.short_description = 'Materia'

