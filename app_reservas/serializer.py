import json
import datetime
from app_reservas.models import Comision, Docente

from django.http import HttpResponse

from app_reservas.models.horario import DIAS_SEMANA

from .errors import not_found_error


def get_materia_json(request, legajo):
    if request.is_ajax():
        json_string = []
        docente_obj = Docente.objects.get(id=legajo)
        docente_comision_qs = docente_obj.docentecomision_set.all()
        for docente_comision in docente_comision_qs:
            json_string.append(
                {
                    'id_materia': docente_comision.comision.materia.id,
                    'id_comision': docente_comision.comision.id,
                    'nombre_materia': docente_comision.comision.materia.nombre,
                    'nombre_comision': docente_comision.comision.comision,
                    'nombre_plan': docente_comision.comision.materia.plan.nombre,
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
        for horario in horarios_qs:
            hora_fin = (datetime.datetime.combine(datetime.date(1, 1, 1), horario.horaInicio) + datetime.timedelta(minutes=horario.duracion)).time()
            json_string.append(
                {
                    'dia_numero': horario.dia,
                    'dia_nombre': DIAS_SEMANA[str(horario.dia)],
                    'hora_inicio': str(horario.horaInicio),
                    'hora_fin': str(hora_fin),
                    'cuatrimestre': horario.comision.cuatrimestre,
                    'cantidad_alumnos': len(horario.comision.alumnocomision_set.all()),
                }
            )

        return HttpResponse(json.dumps(json_string), content_type='application/json')
    else:
        return not_found_error(request)
