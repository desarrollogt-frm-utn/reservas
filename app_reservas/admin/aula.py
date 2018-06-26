# coding=utf-8

from django.contrib import admin
from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.conf import settings
import os
from celery import group

from app_reservas.tasks import obtener_eventos_recurso_especifico

from ..models import Aula


@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de Aula en la interfaz de administración.
    """
    list_display = (
        '_nombre',
        'capacidad',
        '_nivel',
        '_cuerpo',
        'archivo_ubicacion',
        '_areas',
        'calendar_codigo',
        'calendar_color',
    )

    list_filter = (
        'nivel',
        'nivel__cuerpo',
        'areas',
    )

    def _nombre(self, obj):
        """
        Obtiene el nombre de la instancia.
        """
        return obj.get_nombre_corto()
    _nombre.short_description = 'Nombre'
    _nombre.admin_order_field = 'numero'

    def _nivel(self, obj):
        """
        Obtiene el nivel asociado a la instancia.
        """
        return obj.nivel.get_nombre_corto()
    _nivel.short_description = 'Nivel'
    _nivel.admin_order_field = 'nivel__numero'

    def _cuerpo(self, obj):
        """
        Obtiene el cuerpo asociado a la instancia.
        """
        return obj.nivel.cuerpo.get_nombre_corto()
    _cuerpo.short_description = 'Cuerpo'
    _cuerpo.admin_order_field = 'nivel__cuerpo__numero'

    def _areas(self, obj):
        """
        Obtiene el listado de áreas asociadas a la instancia.
        """
        return ", ".join([area.nombre for area in obj.areas.all()])
    _areas.short_description = 'Áreas'


    def get_urls(self):
        urls = super(AulaAdmin, self).get_urls()
        add_urls = [
            url(
                r'^actualizar/$',
                self.admin_site.admin_view(self.actulizar),
                name='app_reservas_aula_actulizar',
            )
        ]

        return add_urls + urls

    def actulizar(self, request):
        context = {
            'site_title': 'Administración de Django',
            'site_header': 'Administración de Django',
            'title': 'Actualizar Calendarios',
            'app_label': self.model._meta.app_label,
            'opts': self.model._meta,
            'has_change_permission': self.has_change_permission(request)
        }

        if request.method == "POST":
            self.actualizar_recursos()
            return redirect(reverse_lazy("admin:%s_%s_changelist" %(self.model._meta.app_label, self.model._meta.model_name)))

        return render(request, 'admin/confirm.html', context)


    def actualizar_recursos(self):
        ruta_archivos = settings.EVENTOS_URL

        # Crea el directorio, en caso de que no exista.
        os.makedirs(ruta_archivos, exist_ok=True)

        # Importación de Aulas, para evitar dependencia circular.
        from app_reservas.models import Aula
        # Obtiene todos los recursos existentes.
        recursos = Aula.objects.all()

        subtareas = group(
            obtener_eventos_recurso_especifico.s(recurso, ruta_archivos)
            for recurso in recursos
        )
        subtareas()
