# coding=utf-8

from django.contrib import admin
from django.conf.urls import url
from django.shortcuts import render, redirect
from app_reservas.tasks import obtener_materias

from ..models import Materia


@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    """
    Especificación de la representación de Materia en la interfaz de administración.
    """
    list_display = (
        'nombre',
        'codigo',
    )

    list_filter = (
        'especialidad',
        'plan',
    )

    def get_urls(self):
        urls = super(MateriaAdmin, self).get_urls()
        add_urls = [
            url(
                r'^actualizar/$',
                self.admin_site.admin_view(self.actulizar),
                name='app_reservas_materia_actulizar',
            )
        ]

        return add_urls + urls

    def actulizar(self, request):
        context = {
            'site_title': 'Administración de Django',
            'site_header': 'Administración de Django',
            'title': 'Actualizar Materias',
            'app_label': self.model._meta.app_label,
            'opts': self.model._meta,
            'has_change_permission': self.has_change_permission(request)
        }

        if request.method == "POST":
            obtener_materias()
            return redirect('admin/app_reservas/materia/')

        return render(request, 'admin/app_reservas/confirm.html', context)