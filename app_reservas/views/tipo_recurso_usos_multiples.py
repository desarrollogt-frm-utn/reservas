# coding=utf-8

from django.views.generic.detail import DetailView

from ..models import TipoRecursoUM


class TipoRecursoUMDetailView(DetailView):
    """
    Vista de detalle para una instancia específica de Tipo de recurso usos múltiples.
    """
    model = TipoRecursoUM
    context_object_name = 'tipo_recurso'
