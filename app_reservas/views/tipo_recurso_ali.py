# coding=utf-8

from django.views.generic.detail import DetailView

from ..models import TipoRecursoAli


class TipoRecursoAliDetailView(DetailView):
    """
    Vista de detalle para una instancia específica de TipoRecursoAli.
    """
    model = TipoRecursoAli
    context_object_name = 'tipo_recurso'


    def get_context_data(self, **kwargs):
        """
        Añade al contexto la lista de recursos activos.
        """
        # Obtiene la información de contexto base.
        context = super(TipoRecursoAliDetailView, self).get_context_data(**kwargs)
        # Busca solo los recursos activos
        filtered_set = self.object.recursoali_set.filter(activo=True)

        context['filtered_set'] = filtered_set
        # Retorna el contexto modificado.
        return context

