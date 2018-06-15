# coding=utf-8

from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from ..models import (
    Cuerpo,
    ImagenContingencia,
    VisorTv,
)


class TvVisorDetailView(DetailView):
    """
    Vista de detalle para la visualización en TV de una instancia específica de
    VisorTv.
    """
    model = VisorTv
    context_object_name = 'visor'
    template_name = 'app_reservas/tv_visor.html'

    def get_object(self, **kwargs):
        """
        Retorna la instancia de VisorTv cuyo slug concuerda con el parámetro
        'slug' de la URL, o una respuesta 404 en caso de ser inválido.
        """
        return get_object_or_404(VisorTv, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        """
        Añade al contexto la información de cuerpo y nivel especificados
        mediante parámetros GET.
        """
        # Obtiene la información de contexto base.
        context = super(TvVisorDetailView, self).get_context_data(**kwargs)
        # Obtiene los parámetros GET de cuerpo y nivel especificados.
        cuerpo = self.request.GET.get('cuerpo')
        nivel = self.request.GET.get('nivel')
        # Convierte los parámetros a entero y los añade al contexto, sólo en
        # caso de que se hayan especificado y sean números.
        if cuerpo and cuerpo.isdigit():
            context['cuerpo_solicitado'] = int(cuerpo)
        if nivel and nivel.isdigit():
            context['nivel_solicitado'] = int(nivel)
        context['texto_pie_pagina'] = self.object.texto_pie_pagina
        # Busca si existe imagenes de contingencia activas
        imagen_contingencia = ImagenContingencia.objects.filter(activo=True)
        if imagen_contingencia:
            context['imagen_contingencia'] = imagen_contingencia[0]
        # Retorna el contexto modificado.
        return context


class TvVisorCuerposDetailView(DetailView):
    """
    Vista de detalle para la visualización en TV de una instancia específica de
    VisorTv, con sus recursos ordenados por cuerpo.
    """
    model = VisorTv
    context_object_name = 'visor'
    template_name = 'app_reservas/tv_visor_cuerpos.html'

    def get_object(self, **kwargs):
        """
        Retorna la instancia de VisorTv cuyo slug concuerda con el parámetro
        'slug' de la URL, o una respuesta 404 en caso de ser inválido.
        """
        return get_object_or_404(VisorTv, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        """
        Añade al contexto la información del pie de página
        """
        # Obtiene la información de contexto base.
        context = super(TvVisorCuerposDetailView, self).get_context_data(**kwargs)
        # Añade la información del pie de página
        context['texto_pie_pagina'] = self.object.texto_pie_pagina
        # Busca si existe imagenes de contingencia activas
        imagen_contingencia = ImagenContingencia.objects.filter(activo=True)
        if imagen_contingencia:
            context['imagen_contingencia'] = imagen_contingencia[0]
        # Retorna el contexto modificado.
        return context


class TvCuerposListView(ListView):
    """
    Vista de lista para la visualización en TV de instancias de Cuerpo,
    ordenadas por número.
    """
    model = Cuerpo
    context_object_name = 'cuerpos'
    template_name = 'app_reservas/tv_cuerpos.html'

    def get_queryset(self):
        """
        Retorna las instancias de Cuerpo cuyo número se encuentra especificado en el parámetro GET
        'numero' de la URL, o todos los cuerpos en caso de que el parámetro no sea especificado.
        Los cuerpos son ordenados por número.
        """
        # Obtiene por parámetro GET 'numero' los números de cuerpos a mostrar. En
        # caso de no especificarse, se muestran todos los cuerpos.
        cuerpos_solicitados = self.request.GET.getlist('numero')

        if cuerpos_solicitados:
            # Filtra los cuerpos para obtener los solicitados.
            cuerpos = Cuerpo.objects.filter(numero__in=cuerpos_solicitados)
        else:
            # Obtiene todos los cuerpos.
            cuerpos = Cuerpo.objects

        # Retorna los cuerpos, ordenados por número (el ordenamiento está definido a nivel de
        # modelo).
        return cuerpos.all()

    def get_context_data(self, **kwargs):
        """
        Añade al contexto la información de nivel especificado mediante
        parámetro GET.
        """
        # Obtiene la información de contexto base.
        context = super(TvCuerposListView, self).get_context_data(**kwargs)
        # Obtiene el parámetro GET de nivel especificado.
        nivel = self.request.GET.get('nivel')
        # Convierte el parámetro a entero y lo añade al contexto, sólo en caso
        # de que se haya especificado y sea número.
        if nivel and nivel.isdigit():
            context['nivel_solicitado'] = int(nivel)
        novedades = []
        for visor in VisorTv.objects.all():
            if visor.texto_pie_pagina:
                novedades.append(visor.get_novedad())
        # Retorna el contexto modificado.
        context['texto_pie_pagina'] = ' | '.join(map(str, novedades))
        # Busca si existe imagenes de contingencia activas
        imagen_contingencia = ImagenContingencia.objects.filter(activo=True)
        if imagen_contingencia:
            context['imagen_contingencia'] = imagen_contingencia[0]
        return context
