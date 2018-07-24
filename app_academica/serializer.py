import json
import datetime
from app_academica.models import Comision

from django.http import HttpResponse

from app_academica.models.horario import DIAS_SEMANA
from app_academica.services.serializerService import get_comisiones_by_legajo

from app_reservas.errors import not_found_error

from reservas.settings.base import WSDL_URL
from suds.client import Client


def get_materia_json(request, legajo):
    if request.is_ajax():

        json_string = []
        comision_qs = get_comisiones_by_legajo(legajo)
        for comision in comision_qs:
            json_string.append(
                {
                    'id_materia': comision.materia.id,
                    'id_comision': comision.id,
                    'nombre_materia': comision.materia.nombre,
                    'nombre_comision': comision.comision,
                    'nombre_plan': comision.materia.plan.nombre,
                }
            )
        return HttpResponse(json.dumps(json_string), content_type='application/json')
    else:
        return not_found_error(request)


def get_horarios_json(request, comision):
    if request.is_ajax():
        json_string = []
        comision_obj = Comision.objects.get(id=comision)
        horarios_qs = comision_obj.horario_set.all()
        cantidad_alumnos = comision_obj.get_cantidad_inscriptos()
        for horario in horarios_qs:
            hora_fin = (datetime.datetime.combine(datetime.date(1, 1, 1), horario.horaInicio) + datetime.timedelta(minutes=horario.duracion)).time()
            json_string.append(
                {
                    'dia_numero': horario.dia,
                    'dia_nombre': DIAS_SEMANA[str(horario.dia)],
                    'hora_inicio': str(horario.horaInicio),
                    'hora_fin': str(hora_fin),
                    'cuatrimestre': horario.comision.cuatrimestre,
                    'cantidad_alumnos': cantidad_alumnos,
                }
            )

        return HttpResponse(json.dumps(json_string), content_type='application/json')
    else:
        return not_found_error(request)


def get_horarios(request):
    url = WSDL_URL
    client = Client(url)

    return HttpResponse(client.service.seticGetHorarios(), content_type='application/json')


def get_alumnos(request):
    url = WSDL_URL
    client = Client(url)

    return HttpResponse(client.service.SeticGetAlumnos(), content_type='application/json')


def get_especialidades(request):
    url = WSDL_URL
    client = Client(url)

    return HttpResponse(client.service.seticGetEspecialidades(), content_type='application/json')


def get_materias(request):
    url = WSDL_URL
    client = Client(url)

    return HttpResponse(client.service.seticGetMaterias(), content_type='application/json')


def get_comisiones_docentes(request, anio):
    url = WSDL_URL
    client = Client(url)

    return HttpResponse(client.service.seticGetComisionesDocentes(anio), content_type='application/json')


def get_cursado(request, anio, legajo):
    url = WSDL_URL
    client = Client(url)

    return HttpResponse(client.service.seticGetCursados(anio, legajo), content_type='application/json')

