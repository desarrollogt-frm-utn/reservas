# coding=utf-8

from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.base import TemplateView

from ..models import CarruselImagenes, Reserva
from app_reservas.models.horarioSolicitud import DIAS_SEMANA
from app_usuarios.models import Docente


class IndexView(TemplateView):
    """
    Vista de plantilla para la página principal de la aplicación.
    """
    template_name = 'app_reservas/index.html'

    def get_context_data(self, **kwargs):
        """
        Añade al contexto el carrusel de imágenes del index.
        """
        # Obtiene la información de contexto base.
        context = super(IndexView, self).get_context_data(**kwargs)
        # Añade el carrusel de imágenes del index, en caso de que exista.
        try:
            carrusel = CarruselImagenes.objects.get(slug='index')

            context['carrusel'] = carrusel
            context['carrusel_imagenes'] = carrusel.imagenes.all()
        except ObjectDoesNotExist:
            pass

        # Retorna el contexto modificado.
        return context


class LoginIndexView(TemplateView):
    """
    Vista de plantilla para la página principal de la aplicación
    estando logeado en el sistema.
    """
    template_name = 'app_reservas/home.html'

    def get_context_data(self, **kwargs):
        """
        Añade al contexto el carrusel de imágenes del index.
        """
        # Obtiene la información de contexto base.
        context = super(LoginIndexView, self).get_context_data(**kwargs)
        # Añade el carrusel de imágenes del index, en caso de que exista.
        try:
            docente_obj = Docente.objects.get(id=self.request.user.id)
            reservas_list = Reserva.objects.filter(docente=docente_obj)[:5]

            context['docente'] = docente_obj
            context['reservas'] = reservas_list
            context['dias_semana'] = DIAS_SEMANA
        except ObjectDoesNotExist:
            pass

        # Retorna el contexto modificado.
        return context
