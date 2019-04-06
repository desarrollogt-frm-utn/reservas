# coding=utf-8

from django import template

from app_reservas.models import TipoRecursoUM
from ..models import (
    Area,
    Cuerpo,
    TipoAula,
    TipoLaboratorio,
    TipoRecursoAli,
)

from app_reservas.utils import obtener_recurso, parse_time, add_minutes_to_time


register = template.Library()


@register.inclusion_tag('app_reservas/navbar.html', takes_context=True)
def obtener_informacion_navbar(context):
    context = {
        'lista_areas': Area.objects.all(),
        'lista_cuerpos': Cuerpo.objects.all(),
        'lista_tipos_laboratorio': TipoLaboratorio.objects.all(),
        'lista_tipos_recurso_ali': TipoRecursoAli.objects.filter(is_visible_navbar=True),
        'user': context.get('user'),
        'lista_tipos_recurso_um': TipoRecursoUM.objects.filter(is_visible_navbar=True),
        'lista_tipos_aulas': TipoAula.objects.filter(is_visible_navbar=True),

    }
    return context

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_horario(horarios, dia):
    for horario in horarios:
        if horario.get('dia_numero') == int(dia):
            return horario
    return None


@register.filter
def get_nombre_recurso(id):
    return str(obtener_recurso(id))

@register.filter
def get_tipo_recurso(id):
    recurso_obj = obtener_recurso(id)
    return recurso_obj.__class__._meta.verbose_name

