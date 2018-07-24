from django.conf import settings
from suds.client import Client
import json
import random
from django.core.cache import cache


from app_academica.mock_response import (
    get_alumnos as mock_alumnos,
    get_comisiones_docentes as mock_docentes,
    get_especialidades as mock_especialidades,
    get_horarios as mock_horarios,
    get_materias as mock_materias
)


def get_horarios():
    if settings.TEST:
        return mock_horarios
    url = settings.WSDL_URL
    client = Client(url)

    json_response = client.service.seticGetHorarios()
    parse_json = json.loads(json_response)

    return parse_json


def get_alumnos():
    if settings.TEST:
        return mock_alumnos
    url = settings.WSDL_URL
    client = Client(url)

    json_response = client.service.SeticGetAlumnos()
    parse_json = json.loads(json_response)

    return parse_json


def get_especialidades():
    if settings.TEST:
        return mock_especialidades
    url = settings.WSDL_URL
    client = Client(url)

    json_response = client.service.seticGetEspecialidades()
    parse_json = json.loads(json_response)

    return parse_json


def get_materias():
    if settings.TEST:
        return mock_materias
    url = settings.WSDL_URL
    client = Client(url)

    json_response = client.service.seticGetMaterias()
    parse_json = json.loads(json_response)

    return parse_json


def get_comisiones_docentes(anio):
    if settings.TEST:
        return mock_docentes
    url = settings.WSDL_URL
    client = Client(url)

    json_response = client.service.seticGetComisionesDocentes(anio)
    parse_json = json.loads(json_response)

    return parse_json


def get_cursado(anio, legajo):
    url = settings.WSDL_URL
    client = Client(url)

    json_response = client.service.seticGetCursados(anio, legajo)
    parse_json = json.loads(json_response)

    return parse_json


def get_cantidad_inscriptos(anio, especialidad, plan, materia, comision):
    if settings.TEST:
        cantidad_inscriptos = random.randint(10, 30)
    else:
        url = settings.WSDL_URL
        client = Client(url)
        cantidad_inscriptos = client.service.seticGetCantidadInscriptos(anio, especialidad, plan, materia, comision)

    response = {
        'cantidad': cantidad_inscriptos
    }

    return response


def get_horarios_comision(anio, especialidad, plan, materia, comision):

    if settings.TEST:
        lista_horarios = cache.get('lista_horarios')
        if not lista_horarios:
            lista_horarios = get_horarios()
            cache.add('lista_horarios', lista_horarios)
        from app_academica.utils import filter_by_comision_materia_especialidad_plan
        return filter_by_comision_materia_especialidad_plan(lista_horarios, comision, materia, especialidad, plan)
    url = settings.WSDL_URL
    client = Client(url)

    json_response = client.service.seticGetHorariosPorComision(anio, especialidad, plan, materia, comision)
    parse_json = json.loads(json_response)

    return parse_json
