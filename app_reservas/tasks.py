# coding=utf-8

import os
import sys
from celery import (
    group,
    shared_task,
)
import json

from app_reservas.adapters.google_calendar import crear_evento

from app_reservas.adapters.frm_utn import get_especialidades, get_materias


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
            especialidad_obj = Especialidad.objects.filter(codigo=especialidad.get('especialid'))
            if not especialidad_obj:
                nombre = especialidad.get('Column1')
                Especialidad.objects.create(
                    codigo=especialidad.get('especialid'),
                    nombre=nombre[:255] if nombre else ""
                )
    except:
        print("Error al obtener especialidades: ", sys.exc_info()[0])
        raise


@shared_task(name='obtener_materias')
def obtener_materias():
    from .models import Materia, Plan, Especialidad
    try:
        json_materias = get_materias()
        for materia in json_materias:
            materia_obj = Materia.objects.filter(codigo=materia.get('especialid'))
            if not materia_obj:
                plan_obj = Plan.objects.filter(nombre=materia.get('plan'))
                especialidad_obj = Especialidad.object.filter(codigo=materia.get('especialid'))
                if not plan_obj:
                    plan_obj = Plan.object.create(nombre=materia.get('plan'))
                if especialidad_obj and plan_obj:
                    nombre = materia.get('Column1')
                    Materia.object.create(
                        codigo=materia.get('especialid'),
                        nombre=nombre[:255] if nombre else "",
                        plan=plan_obj,
                        especialidad=especialidad_obj
                    )
    except:
        print("Error al obtener materias: ", sys.exc_info()[0])
        raise
