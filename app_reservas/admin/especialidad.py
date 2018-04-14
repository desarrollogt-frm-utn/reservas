# coding=utf-8

from django.contrib import admin
from django.conf.urls import url
from django.shortcuts import render, redirect
from app_reservas.tasks import obtener_especialidades

from ..models import Especialidad


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de Especialidad en la interfaz de administración.
    """
    list_display = (
        'nombre',
        'descripcion',
    )


    def get_urls(self):
        urls = super(EspecialidadAdmin, self).get_urls()
        add_urls = [
            url(
                r'^actualizar/$',
                self.admin_site.admin_view(self.actulizar),
                name='app_reservas_especialidad_actulizar',
            )
        ]

        return add_urls + urls

    def actulizar(self, request):
        context = {
            'site_title': 'Administración de Django',
            'site_header': 'Administración de Django',
            'title': 'Actualizar Especilidades',
            'app_label': self.model._meta.app_label,
            'opts': self.model._meta,
            'has_change_permission': self.has_change_permission(request)
        }

        if request.method == "POST":
            obtener_especialidades()
            return redirect('admin/app_reservas/especialidad/')

        return render(request, 'admin/app_reservas/confirm.html', context)