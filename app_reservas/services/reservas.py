from django.db.models import Q
from django.utils import timezone

from app_reservas.models import HistoricoEstadoReserva, Reserva, HorarioReserva
from app_reservas.models.historicoEstadoReserva import ESTADOS_FINALES
from app_reservas.services.recursos import get_recurso_obj
from app_reservas.tasks import crear_evento_recurso_especifico, obtener_eventos_recurso_especifico

from app_reservas.utils import (
    obtener_siguiente_dia_vigente,
    obtener_fecha_finalizacion_reserva_cursado,
    obtener_fecha_finalizacion_reserva_fuera_cursado,
    get_now_timezone)

from app_reservas.adapters.google_calendar import borrar_evento

from app_usuarios.models import Usuario as UsuarioModel


def get_nombre_evento(docente_obj, comision_obj):
    if comision_obj is not None:
        titulo = "{0!s} - {1!s} - {2!s}".format(comision_obj.materia.nombre, comision_obj.comision,
                                                docente_obj.nombre)
    else:
        titulo = "Solicitud fuera de agenda - {0!s}".format(docente_obj.nombre)
    return titulo


def crear_evento(reserva_obj):
    for horario_obj in reserva_obj.horarioreserva_set.all():
        inicio = obtener_siguiente_dia_vigente(int(horario_obj.dia), horario_obj.inicio, reserva_obj.fecha_inicio)
        fin = obtener_siguiente_dia_vigente(int(horario_obj.dia), horario_obj.fin, reserva_obj.fecha_inicio)
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
        estado_antiguo.fecha_fin = get_now_timezone()
        estado_antiguo.save()
        HistoricoEstadoReserva.objects.create(
            fecha_inicio=get_now_timezone(),
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


def crear_reserva_rapida(recurso, docente_obj, comision_obj, asignado_por, hora_fin):
    try:
        user_model_obj = UsuarioModel.objects.get(legajo=docente_obj.legajo)
    except UsuarioModel.DoesNotExist:
        user_model_obj = None

    reserva_obj = Reserva.objects.create(
        fecha_inicio=get_now_timezone(),
        nombre_evento=get_nombre_evento(docente_obj, comision_obj),
        asignado_por=asignado_por,
        recurso=recurso,
        docente=docente_obj,
        comision=comision_obj,
        usuario=user_model_obj
    )

    HistoricoEstadoReserva.objects.create(
        fecha_inicio=get_now_timezone(),
        estado='1',
        reserva=reserva_obj,
    )
    from datetime import datetime

    horario_reserva_obj = HorarioReserva.objects.create(
        inicio=get_now_timezone(),
        fin=hora_fin,
        reserva=reserva_obj,
        dia=get_now_timezone().weekday()
    )
    recurso_obj = get_recurso_obj(recurso.id)

    if recurso_obj:
        fin = datetime.combine(get_now_timezone().date(), hora_fin).isoformat()
        crear_evento_recurso_especifico.delay(
            calendar_id=recurso_obj.calendar_codigo,
            titulo=reserva_obj.nombre_evento,
            inicio=get_now_timezone().isoformat(),
            fin=fin,
            hasta=None,
            reserva_horario_obj=horario_reserva_obj
        )

    return reserva_obj


def buscar_reservas(base_recurso_obj, fecha, hora_inicio, hora_fin=None):

    reserva_list = []

    recurso_obj = get_recurso_obj(base_recurso_obj.id)
    if recurso_obj:
        reserva_qs = recurso_obj.get_active_reservations()
        dia_reserva = fecha.weekday()
        reserva_qs = reserva_qs.filter(
            horarioreserva__dia=dia_reserva
        )

        for reserva in reserva_qs:
            horario_obj = reserva.get_horario_de_fecha(fecha)
            if (horario_obj.inicio <= hora_inicio <= horario_obj.fin) or \
                    (hora_fin and horario_obj.inicio <= hora_fin <= horario_obj.fin):
                reserva_list.append(reserva)

    else:
        prestamo_obj = base_recurso_obj.get_active_loan()
        if prestamo_obj:
            reserva_list = prestamo_obj.recursos_all.filter(recurso=base_recurso_obj)
    return reserva_list


def buscar_reservas_por_hora(base_recurso_obj, fecha_inicio, fecha_fin,  dia_reserva, hora_inicio, hora_fin=None):

    reserva_list = []

    recurso_obj = get_recurso_obj(base_recurso_obj.id)
    if recurso_obj:
        reserva_qs = recurso_obj.buscar_reservas_activas_por_fechas(recurso_obj, fecha_inicio, fecha_fin, dia_reserva)

        for reserva in reserva_qs:
            horario_obj = reserva.horarioreserva_set.get(dia=dia_reserva)
            if (horario_obj.inicio <= hora_inicio <= horario_obj.fin) or \
                    (hora_fin and horario_obj.inicio <= hora_fin <= horario_obj.fin):
                reserva_list.append(reserva)

    else:
        prestamo_obj = base_recurso_obj.get_active_loan()
        if prestamo_obj:
            reserva_list = prestamo_obj.recursos_all.filter(recurso=base_recurso_obj)
    return reserva_list


def buscar_reservas_activas_por_fechas(base_recurso_obj, fecha_inicio, fecha_fin=None, dia_reserva=None):
    reserva_list = []

    recurso_obj = get_recurso_obj(base_recurso_obj.id)

    if recurso_obj and fecha_inicio:
        reserva_list = Reserva.objects.filter(
            recurso__id=recurso_obj.id,
            historicoestadoreserva__estado='1',
            historicoestadoreserva__fecha_fin__isnull=True,
            fecha_inicio__lte=fecha_inicio,
            fecha_fin__gte=fecha_inicio
        )
        if fecha_fin:
            reserva_list = reserva_list.filter(
                fecha_inicio__lte=fecha_fin, fecha_fin__gte=fecha_fin
            )

        if dia_reserva:
            reserva_list = reserva_list.filter(
                horarioreserva__dia=dia_reserva
            )

    else:
        prestamo_obj = base_recurso_obj.get_active_loan()
        if prestamo_obj:
            reserva_list = prestamo_obj.recursos_all.filter(recurso=base_recurso_obj)
    return reserva_list
