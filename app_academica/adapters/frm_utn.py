from django.conf import settings
from suds.client import Client
import json
import random


def get_horarios():
    url = settings.WSDL_URL
    client = Client(url)

    json_response = client.service.seticGetHorarios()
    parse_json = json.loads(json_response)

    return parse_json


def get_alumnos():
    url = settings.WSDL_URL
    client = Client(url)

    json_response = client.service.SeticGetAlumnos()
    parse_json = json.loads(json_response)

    return parse_json


def get_especialidades():
    url = settings.WSDL_URL
    client = Client(url)

    json_response = client.service.seticGetEspecialidades()
    parse_json = json.loads(json_response)

    return parse_json


def get_materias():
    url = settings.WSDL_URL
    client = Client(url)

    json_response = client.service.seticGetMaterias()
    parse_json = json.loads(json_response)

    return parse_json


def get_comisiones_docentes(anio):
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
    url = settings.WSDL_URL
    client = Client(url)

    json_response = client.service.seticGetHorariosPorComision(anio, especialidad, plan, materia, comision)
    parse_json = json.loads(json_response)

    return parse_json
