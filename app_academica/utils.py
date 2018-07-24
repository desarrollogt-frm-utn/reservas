from django.utils import timezone


def filter_by_comision_materia_especialidad_plan(list_json, comision, materia, especialidad, plan):
    return [i for i in list_json if str(i['comision']) == str(comision)
            and str(i['materia']) == str(materia)
            and str(i['especialid']) == str(especialidad)
            and str(i['plan']) == str(plan)
            ]


def filter_by_legajo(list_json, legajo):
    return [i for i in list_json if str(i['legajo']) == str(legajo)]


def obtener_anio_academico():
    return timezone.now().year


def obtener_comision_by_esp_mat_com_plan(especialidad, materia, comision, plan):
    from .models import Comision
    materia_obj = obtener_materia_by_esp_mat_plan(especialidad, materia, plan)

    if materia_obj:
        comision_list = Comision.objects.filter(
            codigo=comision,
            materia=materia_obj,
            anioacademico=obtener_anio_academico()
        )
        if comision_list:
            return comision_list[0]

    return None


def obtener_materia_by_esp_mat_plan(especialidad, materia, plan):
    from .models import Especialidad, Materia, Plan

    especialidad_list = Especialidad.objects.filter(codigo=especialidad)
    plan_list = Plan.objects.filter(nombre=plan)
    if especialidad_list and plan_list:
        especialidad_obj = especialidad_list[0]
        plan_obj = plan_list[0]
        materia_list = Materia.objects.filter(
            codigo=materia,
            especialidad=especialidad_obj,
            plan=plan_obj
        )
        if materia_list:
            return materia_list[0]

    return None
