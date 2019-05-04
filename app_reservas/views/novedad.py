from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.core.exceptions import ObjectDoesNotExist


from ..models import (
    Novedad,
    CarruselImagenes
)

class NovedadView(DetailView):
    """
    Vista de detalle para la visualización de novedades
    """
    model = Novedad
    context_object_name = 'novedad'
    template_name = 'app_reservas/novedad.html'

    def get_object(self, **kwargs):
        """
        Retorna la instancia de Novedad cuyo slug concuerda con el parámetro
        'slug' de la URL, o una respuesta 404 en caso de ser inválido.
        """
        return get_object_or_404(Novedad, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        """
        Añade al contexto el carrusel de imágenes de la novedad.
        """
        # Obtiene la información de contexto base.
        context = super(NovedadView, self).get_context_data(**kwargs)
        # Añade el carrusel de imágenes de la novedad, en caso de que exista.
        try:
            if self.object.carrusel:
                carrusel = CarruselImagenes.objects.get(slug=self.object.carrusel.slug)


                context['carrusel'] = carrusel
                context['carrusel_imagenes'] = carrusel.imagenes.all()
        except ObjectDoesNotExist:
            pass

        # Retorna el contexto modificado.
        return context