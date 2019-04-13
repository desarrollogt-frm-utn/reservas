# coding=utf-8

from django.core.exceptions import ImproperlyConfigured
from django.views.generic.detail import DetailView

from ..models import Aula, Area, TipoAula


class AulaDetailView(DetailView):
    """
    Vista de detalle para una instancia específica de Aula.
    """
    model = Aula
    context_object_name = 'aula'



class CustomAulaDetailView(DetailView):
    """
    Vista de detalle para aulas filtradasx.
    """
    model = Area
    context_object_name = 'model'
    template_name = 'app_reservas/aulas_custom_model_detail.html'


    def get_queryset(self):
        model_param = self.kwargs.get('model')

        if model_param == 'aulas':
            self.model = TipoAula
        elif model_param == 'area':
            self.model = Area
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )

        if self.queryset is None:
            if self.model:
                return self.model._default_manager.all()
        return self.queryset.all()


    def get_context_data(self, **kwargs):
        """
        Añade al contexto la lista de recursos activos.
        """
        # Obtiene la información de contexto base.
        context = super(CustomAulaDetailView, self).get_context_data(**kwargs)
        # Busca solo los recursos activos
        filtered_set = self.object.get_aulas().filter(activo=True)

        context['filtered_set'] = filtered_set
        # Retorna el contexto modificado.
        return context
