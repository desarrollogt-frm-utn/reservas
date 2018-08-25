# coding=utf-8

import sys
import traceback
from celery import (
    shared_task,
)

from app_academica.adapters.frm_utn import get_especialidades, get_materias, get_comisiones_docentes, get_horarios
from app_academica.utils import obtener_anio_academico, obtener_comision_by_esp_mat_com_plan, obtener_materia_by_esp_mat_plan


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
                print("Error al guardar materia: ", sys.exc_info()[0], traceback.print_exc())
    except:
        print("Error al obtener materias: ", sys.exc_info()[0], traceback.print_exc())
        raise


@shared_task(name='obtener_comisiones')
def obtener_comisiones():
    from .models import Comision
    try:
        json_horarios = get_horarios()
        for horario in json_horarios:
            comision_obj = obtener_comision_by_esp_mat_com_plan(
                horario.get('especialid'),
                horario.get('materia'),
                horario.get('comision'),
                horario.get('plan')
            )
            try:
                if not comision_obj:
                    comision_str = horario.get('curso').replace(' ', '')

                    materia_obj = obtener_materia_by_esp_mat_plan(
                        horario.get('especialid'),
                        horario.get('materia'),
                        horario.get('plan')
                    )
                    if materia_obj:
                        Comision.objects.create(
                            comision=comision_str,
                            anioacademico=obtener_anio_academico(),
                            codigo=horario.get('comision'),
                            semestre=horario.get('cuatrimest'),
                            materia=materia_obj
                        )


            except:
                print("Error al guardar la comision: ", sys.exc_info()[0], traceback.print_exc())
    except:
        print("Error al obtener comisiones: ", sys.exc_info()[0], traceback.print_exc())
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
                traceback.print_exc()
    except:
        print("Error al obtener docentes: ", sys.exc_info()[0])
        raise
