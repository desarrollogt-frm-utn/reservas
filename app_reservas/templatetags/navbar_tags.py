# coding=utf-8

from django import template

from ..models import (
    Area,
    Cuerpo,
    TipoLaboratorio,
    TipoRecursoAli,
)


register = template.Library()


@register.inclusion_tag('app_reservas/navbar.html', takes_context=True)
def obtener_informacion_navbar(context):
    context = {
        'lista_areas': Area.objects.all(),
        'lista_cuerpos': Cuerpo.objects.all(),
        'lista_tipos_laboratorio': TipoLaboratorio.objects.all(),
        'lista_tipos_recurso_ali': TipoRecursoAli.objects.filter(is_visible_navbar=True),
        'user': context.get('user')
    }
    return context

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
