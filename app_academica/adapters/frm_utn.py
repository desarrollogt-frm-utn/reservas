from django.conf import settings
from suds.client import Client
import json
from django.core.cache import cache


def get_horarios(from_cache=True):
    if from_cache:
        get_horarios_cache = cache.get('get_horarios')
        if get_horarios_cache:
            return json.loads(get_horarios_cache)

    url = settings.WSDL_URL
    client = Client(url)
    json_response = client.service.seticGetHorarios()
    cache.add('get_horarios', json_response)
    parse_json = json.loads(json_response)

    return parse_json


def get_alumnos(from_cache=True):
    if from_cache:
        get_alumnos_cache = cache.get('get_alumnos')
        if get_alumnos_cache:
            return json.loads(get_alumnos_cache)
    url = settings.WSDL_URL
    client = Client(url)

    json_response = client.service.SeticGetAlumnos()
    cache.add('get_alumnos', json_response)
    parse_json = json.loads(json_response)

    return parse_json


def get_especialidades(from_cache=True):
    if from_cache:
        get_especialidades_cache = cache.get('get_especialidades')
        if get_especialidades_cache:
            return json.loads(get_especialidades_cache)
    url = settings.WSDL_URL
    client = Client(url)

    json_response = client.service.seticGetEspecialidades()
    cache.add('get_especialidades', json_response)
    parse_json = json.loads(json_response)

    return parse_json


def get_materias(from_cache=True):
    if from_cache:
        get_materias_cache = cache.get('get_materias')
        if get_materias_cache:
            return json.loads(get_materias_cache)
    url = settings.WSDL_URL
    client = Client(url)

    json_response = client.service.seticGetMaterias()
    cache.add('get_materias', json_response)
    parse_json = json.loads(json_response)

    return parse_json


def get_comisiones_docentes(anio, from_cache=True):
    if from_cache:
        get_comisiones_docentes_cache = cache.get('get_especialidades_{0!s}'.format(anio))
        if get_comisiones_docentes_cache:
            return json.loads(get_comisiones_docentes_cache)
    url = settings.WSDL_URL
    client = Client(url)

    json_response = client.service.seticGetComisionesDocentes(anio)
    cache.add('get_especialidades_{0!s}'.format(anio), json_response)
    parse_json = json.loads(json_response)

    return parse_json


def get_cursado(anio, legajo):
    url = settings.WSDL_URL
    client = Client(url)

    json_response = client.service.seticGetCursados(anio, legajo)
    parse_json = json.loads(json_response)

    return parse_json


def get_cantidad_inscriptos(anio, especialidad, plan, materia, comision, from_cache=True):
    cantidad_inscriptos = None
    if from_cache:
        get_comisiones_docentes_cache = cache.get('get_cantidad_inscriptos_{0!s}_{1!s}_{2!s}_{3!s}_{4!s}'.format(
            anio,
            especialidad,
            plan,
            materia,
            comision
        ))
        if get_comisiones_docentes_cache:
            cantidad_inscriptos = get_comisiones_docentes_cache

    if not cantidad_inscriptos:
        url = settings.WSDL_URL
        client = Client(url)
        cantidad_inscriptos = client.service.seticGetCantidadInscriptos(anio, especialidad, plan, materia, comision)
        cache.add('get_cantidad_inscriptos_{0!s}_{1!s}_{2!s}_{3!s}_{4!s}'.format(
            anio,
            especialidad,
            plan,
            materia,
            comision
        ), cantidad_inscriptos)

    response = {
        'cantidad': cantidad_inscriptos
    }

    return response


def get_horarios_comision(anio, especialidad, plan, materia, comision, from_cache=True):
    if from_cache:
        get_horarios_comision_cache = cache.get('get_horarios_comision_{0!s}_{1!s}_{2!s}_{3!s}_{4!s}'.format(
            anio,
            especialidad,
            plan,
            materia,
            comision
        ))
        if get_horarios_comision_cache:
            return json.loads(get_horarios_comision_cache)

    url = settings.WSDL_URL
    client = Client(url)

    json_response = client.service.seticGetHorariosPorComision(anio, especialidad, plan, materia, comision)
    cache.add('get_horarios_comision_{0!s}_{1!s}_{2!s}_{3!s}_{4!s}'.format(
        anio,
        especialidad,
        plan,
        materia,
        comision
    ), json_response)
    parse_json = json.loads(json_response)

    return parse_json
