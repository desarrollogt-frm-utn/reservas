# coding=utf-8

from django import template

from app_reservas.models import TipoRecursoSAE
from ..models import (
    Area,
    Cuerpo,
    TipoLaboratorio,
    TipoRecursoAli,
)


register = template.Library()


@register.inclusion_tag('app_reservas/navbar.html')
def obtener_informacion_navbar():
    context = {
        'lista_areas': Area.objects.all(),
        'lista_cuerpos': Cuerpo.objects.all(),
        'lista_tipos_laboratorio': TipoLaboratorio.objects.all(),
        'lista_tipos_recurso_ali': TipoRecursoAli.objects.filter(is_visible_navbar=True),
        'lista_tipos_recurso_sae': TipoRecursoSAE.objects.filter(is_visible_navbar=True)
    }
    return context
