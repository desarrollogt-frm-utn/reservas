import datetime

from django.utils import timezone

from app_reservas.models import HistoricoEstadoReserva
from app_reservas.models.historicoEstadoReserva import ESTADOS_FINALES
from app_reservas.services.recursos import get_recurso_obj
from app_reservas.tasks import crear_evento_recurso_especifico, obtener_eventos_recurso_especifico

from app_reservas.utils import (
    obtener_siguiente_dia_vigente,
    obtener_fecha_finalizacion_reserva_cursado,
    obtener_fecha_finalizacion_reserva_fuera_cursado
)

from app_reservas.adapters.google_calendar import borrar_evento

def get_nombre_evento(docente_obj, comision_obj):
    if comision_obj is not None:
        titulo = "{0!s} - {1!s} - {2!s}".format(comision_obj.materia.nombre, comision_obj.comision,
                                                docente_obj.nombre)
    else:
        titulo = "Solicitud fuera de agenda - {0!s}".format(docente_obj.nombre)
    return titulo


def crear_evento(reserva_obj):
    for horario_obj in reserva_obj.horarioreserva_set.all():
        inicio = obtener_siguiente_dia_vigente(int(horario_obj.dia), horario_obj.inicio)
        fin = obtener_siguiente_dia_vigente(int(horario_obj.dia), horario_obj.fin)
        hasta = None

        if reserva_obj.comision and reserva_obj.fecha_fin:
            hasta = obtener_fecha_finalizacion_reserva_cursado(reserva_obj.comision.semestre)
        elif not reserva_obj.comision and reserva_obj.fecha_fin:
            hasta = obtener_fecha_finalizacion_reserva_fuera_cursado(reserva_obj.fecha_fin)

        recurso_obj = get_recurso_obj(reserva_obj.recurso.id)
        if recurso_obj:
            crear_evento_recurso_especifico(
                calendar_id=recurso_obj.calendar_codigo,
                titulo=reserva_obj.nombre_evento,
                inicio=inicio,
                fin=fin,
                hasta=hasta,
                reserva_horario_obj=horario_obj,
            )

"""
ESTADOS RESERVA
    1: Activa,
    2: Finalizada,
    3: Dada de baja por usuario,
    4: Dada de baja por bedel,
}
"""

def cambiar_estado_reserva(reserva_obj, estado_nuevo):
    estado_antiguo = reserva_obj.get_estado_reserva()
    if estado_antiguo and estado_antiguo not in ESTADOS_FINALES:
        estado_antiguo.fecha_fin = timezone.now()
        estado_antiguo.save()
        HistoricoEstadoReserva.objects.create(
            fecha_inicio=timezone.now(),
            estado=estado_nuevo,
            reserva=reserva_obj,
        )
    else:
        raise ValueError('El recurso se encuentra en un estado final')


def dar_baja_evento(reserva_obj):
    cambiar_estado_reserva(reserva_obj, '4')
    recurso_obj = get_recurso_obj(reserva_obj.recurso.id)
    if recurso_obj:
        for horario_reserva in reserva_obj.horarioreserva_set.all():
            borrar_evento(recurso_obj.calendar_codigo, horario_reserva.id_evento_calendar)
        obtener_eventos_recurso_especifico(recurso_obj)


def finalizar_reserva(reserva_obj):
    if not reserva_obj.fecha_fin or (reserva_obj and reserva_obj.fecha_fin <= timezone.now().date()):
        cambiar_estado_reserva(reserva_obj, '2')
