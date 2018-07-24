# coding=utf-8

import os
from celery import (
    group,
    shared_task,
)
import json
from django.conf import settings

from app_reservas.adapters.google_calendar import crear_evento


@shared_task(name='obtener_eventos_recursos')
def obtener_eventos_recursos():
    # Indica la ruta donde se almacenarán los archivos.
    ruta_archivos = settings.EVENTOS_URL

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
    ruta_archivos=settings.EVENTOS_URL
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
def crear_evento_recurso_especifico(calendar_id, titulo, inicio, fin, hasta, reserva_horario_obj=None):
    evento = crear_evento(
        calendar_id=calendar_id,
        titulo=titulo,
        inicio=inicio,
        fin=fin,
        hasta=hasta
    )

    if reserva_horario_obj:
        reserva_horario_obj.id_evento_calendar = evento.get('id')
        reserva_horario_obj.save()

    from .models import Recurso
    recurso_obj = Recurso.objects.get(calendar_codigo=calendar_id)
    obtener_eventos_recurso_especifico(recurso_obj)