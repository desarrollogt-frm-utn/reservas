from app_academica.constants import DIAS_SEMANA
from app_academica.models import Comision
from app_academica.utils import filter_by_legajo, obtener_anio_academico, obtener_comision_by_esp_mat_com_plan, \
    filter_by_comision_materia_especialidad_plan
from app_academica.adapters.frm_utn import get_comisiones_docentes, get_horarios_comision

from app_reservas.utils import parse_time, add_minutes_to_time


def get_comisiones_by_legajo(legajo):
    comision_list = []
    docente_comisiones_list = filter_by_legajo(
        get_comisiones_docentes(obtener_anio_academico()),
        legajo)

    for comision_json in docente_comisiones_list:
        comision_obj = obtener_comision_by_esp_mat_com_plan(
            comision_json.get('especialid'),
            comision_json.get('materia'),
            comision_json.get('comision'),
            comision_json.get('plan')
        )
        if comision_obj:
            comision_list += [comision_obj]

    return comision_list


def get_docentes_by_comision_materia_especialidad_plan(comision, materia, especialidad, plan):
    docente_list = filter_by_comision_materia_especialidad_plan(
        get_comisiones_docentes(obtener_anio_academico()),
        comision,
        materia,
        especialidad,
        plan
    )

    return docente_list


def get_comision_response(comision):
    comision_json = {}
    comision_list = Comision.objects.filter(id=comision)
    if comision_list:
        comision_obj = comision_list[0]

        comision_json = {
            'anioacademico': comision_obj.anioacademico,
            'comision': comision_obj.comision,
            'semestre': comision_obj.semestre,
            'cantidad_alumnos': comision_obj.get_cantidad_inscriptos(),
            'materia': comision_obj.materia.nombre,
            'especialidad': comision_obj.materia.especialidad.nombre,
            'horarios': get_horarios_comision_list(comision_obj),

        }

    return comision_json


def get_horarios_comision_list(comision_obj):
    horarios_academicos_list = get_horarios_comision(
        comision_obj.anioacademico,
        comision_obj.materia.especialidad.codigo,
        comision_obj.materia.plan.nombre,
        comision_obj.materia.codigo,
        comision_obj.codigo
    )

    horarios_list = []
    for horario in horarios_academicos_list:
        hora_inicio = parse_time(horario.get('horacomien'))
        hora_fin = add_minutes_to_time(hora_inicio, horario.get('duracion'))
        parsed_horario = {
            'hora_inicio': hora_inicio.strftime("%H:%M"),
            'hora_fin': hora_fin.strftime("%H:%M"),
            'dia_numero': horario.get('dia'),
            'dia_nombre': DIAS_SEMANA[str(horario.get('dia'))],
        }
        horarios_list += [parsed_horario]

    return horarios_list
