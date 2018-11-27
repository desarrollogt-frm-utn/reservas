import datetime
import json

from constance import config
from django.utils import timezone
from rolepermissions.checkers import has_permission, has_role

from app_reservas.roles import ASSIGN_RECURSO_AULA, ASSIGN_RECURSO_ALI, ASSIGN_RECURSO_LABORATORIO, \
    ASSIGN_RECURSO_LABORATORIO_INFORMATICO, ADMINISTRADOR_ROLE


def obtener_siguiente_dia_vigente(dia, horario):
    now = get_now_timezone()

    if now.weekday() == dia:
        return datetime.datetime.combine(now.date(), horario).isoformat()
    elif now.weekday() < dia:
        dia = now.date() + datetime.timedelta(days=dia-now.weekday())
    else:
        dia = now.date() + datetime.timedelta(days=6-(now.weekday()-dia))
    return datetime.datetime.combine(dia, horario).isoformat()


def obtener_fecha_finalizacion_reserva_cursado(semestre):
    if semestre == '1':
        fecha_fin = config.FECHA_FIN_PRIMER_SEMESTRE
        if fecha_fin.year == get_now_timezone().year:
            return datetime.datetime.combine(fecha_fin, datetime.time(23, 00)).strftime("%Y%m%dT%H%M%SZ")
        else:
            return timezone.datetime(get_now_timezone().year, 6, 25, 23, 00).strftime("%Y%m%dT%H%M%SZ")
    if semestre == '2' or semestre == '0':
        fecha_fin = config.FECHA_FIN_SEGUNDO_SEMESTRE
        if fecha_fin.year == get_now_timezone().year:
            return datetime.datetime.combine(fecha_fin, datetime.time(23, 00)).strftime("%Y%m%dT%H%M%SZ")
        else:
            return timezone.datetime(get_now_timezone().year, 11, 30, 23, 00).strftime("%Y%m%dT%H%M%SZ")


def obtener_fecha_finalizacion_reserva_fuera_cursado(date):
    return datetime.datetime.combine(date, datetime.time(23, 00)).strftime("%Y%m%dT%H%M%SZ")


def obtener_fecha_inicio_reserva_cursado(semestre):
    if semestre == '1' or semestre == '0':
        fecha_inicio = config.FECHA_INICIO_PRIMER_SEMESTRE
        if fecha_inicio.year == get_now_timezone().year:
            return fecha_inicio
        else:
            return timezone.datetime(get_now_timezone().year, 3, 8,)
    if semestre == '2':
        fecha_inicio = config.FECHA_INICIO_SEGUNDO_SEMESTRE
        if fecha_inicio.year == get_now_timezone().year:
            return fecha_inicio
        else:
            return timezone.datetime(get_now_timezone().year, 8, 8,)


def obtener_fecha_fin_reserva_cursado(semestre):
    if semestre == '1':
        fecha_fin = config.FECHA_FIN_PRIMER_SEMESTRE
        if fecha_fin.year == get_now_timezone().year:
            return fecha_fin
        else:
            return timezone.datetime(get_now_timezone().year, 6, 25,)
    if semestre == '2' or semestre == '0':
        fecha_fin = config.FECHA_FIN_SEGUNDO_SEMESTRE
        if fecha_fin.year == get_now_timezone().year:
            return fecha_fin
        else:
            return timezone.datetime(get_now_timezone().year, 12, 19,)


def obtener_modelo_recurso(id):
    from app_reservas.models import Aula, Accesorio, Laboratorio, LaboratorioInformatico, RecursoAli
    if Aula.objects.filter(id=id):
        return Aula
    elif LaboratorioInformatico.objects.filter(id=id):
        return LaboratorioInformatico
    elif Laboratorio.objects.filter(id=id):
        return Laboratorio
    elif RecursoAli.objects.filter(id=id):
        return RecursoAli
    elif Accesorio.objects.filter(id=id):
        return Accesorio
    else:
        return None


def obtener_recurso(id):
    model = obtener_modelo_recurso(id)
    if model:
        return model.objects.filter(id=id)[0]
    return None


def parse_time(time):
    str_time = str(time)
    if len(str_time) > 2:
        hora = "{0!s}:{1!s}".format(str_time[:-2], str_time[-2:])
    elif len(str_time) <= 2:
        hora = "{0!s}:00".format(str_time)
    return timezone.datetime.strptime(hora, "%H:%M").time()


def add_minutes_to_time(time, minutes):
    hora = (datetime.datetime.combine(datetime.date(1, 1, 1), time) + datetime.timedelta(
        minutes=minutes))
    return hora.time()


def parse_eventos_response(eventos, resource_id):
    eventos_json = '['
    primera_iteracion = True
    for evento in eventos:
        if primera_iteracion:
            primera_iteracion = False
        else:
            eventos_json += ',\n'
        evento_str = json.dumps({
            'title': evento['titulo'],
            'start': evento['inicio_str'],
            'end': evento['fin_str'],
            'resourceId': resource_id
        })
        eventos_json += evento_str
    eventos_json += ']'
    return eventos_json


def obtener_recursos_asignables(user):
    from app_reservas.models import Recurso, Aula, Laboratorio, LaboratorioInformatico, RecursoAli
    from app_usuarios.models import Usuario
    recurso_list = []

    if not user:
        return recurso_list

    if has_role(user, ADMINISTRADOR_ROLE):
        return list(Recurso.objects.all())

    if has_permission(user, ASSIGN_RECURSO_AULA):
        usuario_model_list = Usuario.objects.filter(pk=user.id)[:1]
        if usuario_model_list:
            usuario_model = usuario_model_list[0]
            aulas_qs = Aula.objects.filter(areas__in=usuario_model.areas.all().values_list('id', flat=True)).distinct()

            recurso_list += list(aulas_qs)

    if has_permission(user, ASSIGN_RECURSO_ALI):
        recurso_list += list(RecursoAli.objects.all())

    if has_permission(user, ASSIGN_RECURSO_LABORATORIO):
        recurso_list += list(Laboratorio.objects.all())

    if has_permission(user, ASSIGN_RECURSO_LABORATORIO_INFORMATICO):
        recurso_list += list(LaboratorioInformatico.objects.all())

    return recurso_list


def obtener_horario_comision(comision, dia_semana=None):
    if comision:
        if not dia_semana:
            dia_semana = get_now_timezone().weekday()
        horario_filtrado = [i for i in comision.get_horarios_comision_academico() if int(i['dia_numero']) == dia_semana]

        if horario_filtrado:
            return horario_filtrado[0]

    return None


def get_now_timezone():
    return timezone.localtime(timezone.now())
