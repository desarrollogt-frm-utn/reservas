# coding=utf-8

from django.views.generic.detail import DetailView

from ..models import TipoRecursoSAE


class TipoRecursoSAEDetailView(DetailView):
    """
    Vista de detalle para una instancia específica de TipoRecursoAli.
    """
    model = TipoRecursoSAE
    context_object_name = 'tipo_recurso'
