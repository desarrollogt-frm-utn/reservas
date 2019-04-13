# coding=utf-8

from django.contrib import admin
from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.conf import settings
import os
from celery import group

from app_reservas.tasks import obtener_eventos_recurso_especifico

from ..models import RecursoAli


@admin.register(RecursoAli)
class RecursoAliAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de RecursoAli en la interfaz de administración.
    """
    list_display = (
        '_identificador',
        'activo',
        '_tipo',
        'calendar_codigo',
        'calendar_color',
    )

    list_filter = (
        'activo',
        'tipo',
    )

    def _identificador(self, obj):
        """
        Obtiene el identificador de la instancia.
        """
        return obj.get_nombre_corto()
    _identificador.short_description = 'Identificador'
    _identificador.admin_order_field = 'identificador'

    def _tipo(self, obj):
        """
        Obtiene el tipo asociado a la instancia.
        """
        return obj.tipo
    _tipo.short_description = 'Tipo'
    _tipo.admin_order_field = 'tipo__nombre'

    def get_urls(self):
        urls = super(RecursoAliAdmin, self).get_urls()
        add_urls = [
            url(
                r'^actualizar/$',
                self.admin_site.admin_view(self.actulizar),
                name='app_reservas_recursoali_actulizar',
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

        # Importación de Recurso, para evitar dependencia circular.
        from app_reservas.models import RecursoAli
        # Obtiene todos los recursos existentes.
        recursos = RecursoAli.objects.all()

        subtareas = group(
            obtener_eventos_recurso_especifico.s(recurso, ruta_archivos)
            for recurso in recursos
        )
        subtareas()
