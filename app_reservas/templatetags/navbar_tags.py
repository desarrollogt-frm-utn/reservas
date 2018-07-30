# coding=utf-8

from django import template

from app_reservas.models import TipoRecursoSAE
from ..models import (
    Area,
    Cuerpo,
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
        'lista_tipos_recurso_sae': TipoRecursoSAE.objects.filter(is_visible_navbar=True),
    }
    return context

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_horario(horarios, dia):
    for horario in horarios:
        if horario.get('dia') == int(dia):
            hora_inicio = parse_time(horario.get('horacomien'))
            horario['hora_inicio'] = hora_inicio
            horario['hora_fin'] = add_minutes_to_time(hora_inicio, horario.get('duracion'))
            return horario
    return None


@register.filter
def get_nombre_recurso(id):
    return str(obtener_recurso(id))
