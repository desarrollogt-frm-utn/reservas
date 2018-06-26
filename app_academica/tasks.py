# coding=utf-8

import sys
from celery import (
    shared_task,
)

from app_academica.adapters.frm_utn import get_especialidades, get_materias, get_comisiones_docentes, get_horarios
from app_academica.utils import filter_by_comision_materia_especialidad, obtener_anio_academico, obtener_comision_by_esp_mat_com_plan, obtener_materia_by_esp_mat_plan

from app_reservas.utils import parse_time

@shared_task(name='obtener_especialidades')
def obtener_especialidades():
    from .models import Especialidad
    try:
        json_especialidades = get_especialidades()
        for especialidad in json_especialidades:
            try:
                especialidad_obj = Especialidad.objects.filter(codigo=especialidad.get('especialid'))
                if not especialidad_obj:
                    nombre = especialidad.get('Column1')
                    Especialidad.objects.create(
                        codigo=especialidad.get('especialid'),
                        nombre=nombre[:255] if nombre else ""
                    )
            except:
                print("Error al guardar especialidad: ", sys.exc_info()[0])
    except:
        print("Error al obtener especialidades: ", sys.exc_info()[0])
        raise


@shared_task(name='obtener_materias')
def obtener_materias():
    from .models import Materia, Plan, Especialidad
    try:
        json_materias = get_materias()
        for materia in json_materias:
            try:
                materia_obj = obtener_materia_by_esp_mat_plan(
                    materia.get('especialid'),
                    materia.get('materia'),
                    materia.get('plan')
                )
                if not materia_obj:
                    especialidad_obj = Especialidad.objects.get(codigo=materia.get('especialid'))
                    plan_list = Plan.objects.filter(nombre=materia.get('plan'))
                    if not plan_list:
                        plan_obj = Plan.objects.create(nombre=materia.get('plan'))
                    else:
                        plan_obj = plan_list[0]
                    if plan_obj:
                        nombre = materia.get('Column1')
                        Materia.objects.create(
                            codigo=materia.get('materia'),
                            nombre=nombre[:255] if nombre else "",
                            plan=plan_obj,
                            especialidad=especialidad_obj
                        )
            except:
                print("Error al guardar materia: ", sys.exc_info()[0])
    except:
        print("Error al obtener materias: ", sys.exc_info()[0])
        raise


@shared_task(name='obtener_comisiones')
def obtener_comisiones():
    from .models import Comision, Horario
    try:
        json_comisiones = get_comisiones_docentes(obtener_anio_academico())
        json_horarios = get_horarios()
        for comision in json_comisiones:
            comision_obj = obtener_comision_by_esp_mat_com_plan(
                comision.get('especialid'),
                comision.get('materia'),
                comision.get('comision'),
                comision.get('plan')
            )
            try:
                if not comision_obj:
                    comision_str = comision.get('curso').replace(' ', '')

                    horario_list = filter_by_comision_materia_especialidad(json_horarios, comision.get('comision'), comision.get('materia'), comision.get('especialid'))
                    if horario_list:
                        materia_obj = obtener_materia_by_esp_mat_plan(
                            comision.get('especialid'),
                            comision.get('materia'),
                            comision.get('plan')
                        )
                        created_comision_obj = Comision.objects.create(
                            comision=comision_str,
                            anioacademico=obtener_anio_academico(),
                            codigo=comision.get('comision'),
                            cuatrimestre=horario_list[0]['cuatrimest'],
                            materia=materia_obj
                        )
                        for horario in horario_list:
                            Horario.objects.create(
                                dia=horario.get('dia'),
                                duracion=horario.get('duracion'),
                                horaInicio=parse_time(horario.get('horacomien')),
                                comision=created_comision_obj
                            )


            except:
                print("Error al guardar la comision: ", sys.exc_info()[0])
    except:
        print("Error al obtener comisiones: ", sys.exc_info()[0])
        raise

@shared_task(name='obtener_docentes')
def obtener_docentes():
    from .models import Docente
    try:
        json_docentes = get_comisiones_docentes(obtener_anio_academico())
        for docente in json_docentes:
            try:
                docente_obj = Docente.objects.filter(legajo=docente.get('legajo'))
                if not docente_obj:
                    Docente.objects.create(
                        nombre=docente.get('nombre'),
                        legajo=docente.get('legajo'),
                        correo=""
                    )
            except:
                print("Error al guardar docente: ", sys.exc_info()[0])
    except:
        print("Error al obtener docentes: ", sys.exc_info()[0])
        raise
