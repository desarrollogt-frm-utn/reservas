from app_academica.utils import filter_by_legajo, obtener_anio_academico, obtener_comision_by_esp_mat_com_plan, \
    filter_by_comision_materia_especialidad_plan
from app_academica.adapters.frm_utn import get_comisiones_docentes


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
