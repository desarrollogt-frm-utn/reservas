# coding=utf-8

import os
import sys
from celery import (
    group,
    shared_task,
)
import json

from django.utils.timezone import datetime
from app_reservas.adapters.google_calendar import crear_evento

from app_reservas.adapters.frm_utn import get_especialidades, get_materias, get_comisiones_docentes, get_horarios
from app_reservas.utils import filter_by_comision_materia_especialidad, parse_time


@shared_task(name='obtener_eventos_recursos')
def obtener_eventos_recursos():
    # Indica la ruta donde se almacenarán los archivos.
    ruta_archivos = 'media/app_reservas/eventos_recursos/'

    # Crea el directorio, en caso de que no exista.
    os.makedirs(ruta_archivos, exist_ok=True)

    # Importación de Recurso, para evitar dependencia circular.
    from .models import Recurso
    # Obtiene todos los recursos existentes.
    recursos = Recurso.objects.all()

    subtareas = group(
        obtener_eventos_recurso_especifico.s(recurso, ruta_archivos)
        for recurso in recursos
    )
    subtareas()


@shared_task(name='obtener_eventos_recurso_especifico')
def obtener_eventos_recurso_especifico(
    recurso,
    ruta_archivos='media/app_reservas/eventos_recursos/'
):
    # Arma el nombre del archivo.
    nombre_archivo = str(recurso.id) + '.json'
    nombre_archivo_completo = ruta_archivos + nombre_archivo

    # Obtiene los eventos del recurso en formato JSON.
    eventos = recurso.get_eventos_json()

    # Verifica que se hayan obtenido eventos, ya que en caso de no obtenerse por algún problema de
    # conexión, no debe sobrescribirse el archivo de eventos del recurso.
    if json.loads(eventos):
        # Crea o sobrescribe el archivo del recurso actual.
        with open(nombre_archivo_completo, 'w') as archivo:
            # Escribe en el archivo los eventos del recurso, en formato JSON.
            archivo.write(eventos)

@shared_task(name='crear_evento_recurso_especifico')
def crear_evento_recurso_especifico(calendar_id, titulo, inicio, fin, hasta):
    crear_evento(
        calendar_id=calendar_id,
        titulo=titulo,
        inicio=inicio,
        fin=fin,
        hasta=hasta
    )

    from .models import Recurso
    recurso_obj = Recurso.objects.get(calendar_codigo=calendar_id)
    obtener_eventos_recurso_especifico(recurso_obj)


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
            #try:
                especialidad_list = Especialidad.objects.filter(codigo=materia.get('especialid'))
                if especialidad_list:
                    especialidad_obj = especialidad_list[0]
                    materia_obj = Materia.objects.filter(codigo=materia.get('materia'), especialidad=especialidad_obj)
                    if not materia_obj:
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
            #except:
               # print("Error al guardar materia: ", sys.exc_info()[0])
    except:
        print("Error al obtener materias: ", sys.exc_info()[0])
        raise


@shared_task(name='obtener_comisiones')
def obtener_comisiones():
    from .models import Comision, Docente, DocenteComision, Especialidad, Horario, Materia
    try:
        json_comisiones = get_comisiones_docentes(datetime.now().year)
        json_horarios = get_horarios()
        for comision in json_comisiones:
            #try:
            especialidad_list = Especialidad.objects.filter(codigo=comision.get('especialid'))
            if especialidad_list:
                especialidad_obj = especialidad_list[0]
                materia_list = Materia.objects.filter(codigo=comision.get('materia'), especialidad=especialidad_obj)
                if materia_list:
                    materia_obj = materia_list[0]
                    comision_str = comision.get('curso').replace(' ', '')
                    comision_obj = Comision.objects.filter(comision=comision_str, materia=materia_obj, anioacademico=datetime.now().year)
                    if not comision_obj:
                        horario_list = filter_by_comision_materia_especialidad(json_horarios, comision.get('comision'), comision.get('materia'), comision.get('especialid'))
                        if horario_list:
                            created_comision_obj = Comision.objects.create(
                                comision=comision_str,
                                anioacademico=datetime.now().year,
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
                            docente_list = filter_by_comision_materia_especialidad(json_comisiones, comision.get('comision'), comision.get('materia'), comision.get('especialid'))
                            for docente in docente_list:
                                docente_list = Docente.objects.filter(legajo=docente.get('legajo'))
                                if not docente_list:
                                    docente_obj = Docente.objects.create(
                                        nombre=docente.get('nombre'),
                                        legajo=docente.get('legajo'),
                                        correo=""
                                    )
                                else:
                                    docente_obj = docente_list[0]

                                DocenteComision.objects.create(
                                    docente=docente_obj,
                                    comision=created_comision_obj,
                                    grado=docente.get('grado')
                                )


            #except:
             #   print("Error al guardar la comision: ", sys.exc_info()[0])
    except:
        print("Error al obtener comisiones: ", sys.exc_info()[0])
        raise
