# coding=utf-8

from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView

from ..models import (
    RecursoUM,
    TipoRecursoUM,
)


class RecursoUMDetailView(DetailView):
    """
    Vista de detalle para una instancia específica de RecursoUM.
    """
    model = RecursoUM
    context_object_name = 'recurso'
    template_name = 'app_reservas/recursoali_detail.html'

    def get_object(self, **kwargs):
        """
        Retorna la instancia de RecursoUM cuyo alias y tipo concuerdan con
        los parámetros 'identificador' y 'tipo' de la URL, o una respuesta 404
        en caso de ser inválido.
        """
        tipo_recurso = get_object_or_404(TipoRecursoUM, slug=self.kwargs['tipo'])
        return get_object_or_404(
            RecursoUM,
            tipo=tipo_recurso,
            slug=self.kwargs['slug'],
        )
