# coding=utf-8
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.base import TemplateView
from django.views.generic import DetailView

from ..models import (
    Aula,
    CarruselImagenes,
    LaboratorioInformatico,
    TipoRecursoAli,
)


class AliTemplateView(TemplateView):
    """
    Vista de plantilla para la página principal del ALI.
    """
    template_name = 'app_reservas/ali_index.html'

    def get_context_data(self, **kwargs):
        """
        Añade al contexto el carrusel de imágenes del index.
        """
        # Obtiene la información de contexto base.
        context = super(AliTemplateView, self).get_context_data(**kwargs)

        # Añade el carrusel de imágenes de la página del ALI, en caso de que exista.
        try:
            carrusel = CarruselImagenes.objects.get(slug='ali_index')

            context['carrusel'] = carrusel
            context['carrusel_imagenes'] = carrusel.imagenes.all()
        except ObjectDoesNotExist:
            pass

        # Añade los tipos de recurso del ALI existentes.
        context['tipos_recurso_ali'] = TipoRecursoAli.objects.all()

        # Añade la cantidad de laboratorios de Informática existentes.
        context['cantidad_laboratorios_informatica'] = LaboratorioInformatico.objects.all().count()

        # Retorna el contexto modificado.
        return context


class AliVideoconferenciasDetailView(DetailView):
    """
    Vista de detalle para la sala de videoconferencias del ALI.
    """
    model = Aula
    context_object_name = 'aula'

    def get_object(self):
        # Obtiene la instancia de la sala de videoconferencias.
        return Aula.objects.filter(
            nivel__cuerpo__numero=6,
            nivel__numero=2,
            numero=1,
        ).first()
