# coding=utf-8
import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.list import ListView

from app_academica.adapters.frm_utn import get_horarios
from app_academica.form import FilterComisionForm
from app_academica.models import Especialidad, Materia, Comision
from app_academica.models.comision import CUATRIMESTRE
from app_academica.models.horario import DIAS_SEMANA_LIST
from app_reservas.templatetags.navbar_tags import get_horario
from app_reservas.utils import parse_time, add_minutes_to_time
from django.db.models import Q

def HorariosWeekView(request):

    horario_response = get_horarios()
    horario_list = []


    for i in range(10):
        horario = horario_response[i]
        especialidad_obj = Especialidad.objects.get(codigo=horario.get('especialid'))
        materia_obj = Materia.objects.get(codigo=horario.get('materia'))
        hora_inicio = parse_time(horario['horacomien'])
        hora_fin = add_minutes_to_time(hora_inicio, horario['duracion'])
        horario_json = {
            'hora_inicio':hora_inicio,
            'dia': horario['dia'],
            'hora_fin': hora_fin,
            'duracion': horario['duracion'],
            'especialidad': especialidad_obj.nombre,
            'materia': materia_obj.nombre,
            'cuatrimestre': horario['cuatrimest']
            }
        horario_list.append(horario_json)



    return render(request, 'app_reservas/horarios_list_week.html', {
            'horarios': horario_list,
        })


class HorariosComisionListView(ListView):
    model = Comision
    template_name = 'app_reservas/horarios_comision_list.html'
    paginate_by = 10
    context_object_name = 'comisiones'

    def get_context_data(self, **kwargs):
        context = super(HorariosComisionListView, self).get_context_data(**kwargs)
        comision_form = FilterComisionForm(self.request.GET)
        context['comision_form'] = comision_form
        context['cuatrimestre'] = CUATRIMESTRE
        context['dias_semana'] = DIAS_SEMANA_LIST
        context['horarios'] = get_horarios()
        return context

    def get_queryset(self):
        especialidad = self.request.GET.get('especialidad', '')
        cuatrimestre = self.request.GET.get('cuatrimestre', '')
        buscar = self.request.GET.get('buscar','')
        comisiones_qs = Comision.objects.filter(materia__especialidad__visible=True)
        if cuatrimestre == '0':
          comisiones_qs = comisiones_qs.filter(
                cuatrimestre=cuatrimestre,
            )
        elif cuatrimestre == '1' or cuatrimestre == '2':
            comisiones_qs = comisiones_qs.filter(
                Q(cuatrimestre=0) | Q(cuatrimestre=cuatrimestre)
            )
        if especialidad:
            try:
                int(especialidad)
                comisiones_qs = comisiones_qs.filter(materia__especialidad__id=especialidad)
            except ValueError:
                pass
        if buscar:
            try:
                comisiones_qs = comisiones_qs.filter(
                Q(materia__nombre__icontains=buscar) | Q(comision__icontains=buscar)
            )
            except ValueError:
                pass
        return comisiones_qs


def horario_descargar(request):
    especialidad = request.GET.get('especialidad', '')
    cuatrimestre = request.GET.get('cuatrimestre', '')
    buscar = request.GET.get('buscar', '')
    comisiones_qs = Comision.objects.filter(materia__especialidad__visible=True)
    if cuatrimestre == '0':
        comisiones_qs = comisiones_qs.filter(
            cuatrimestre=cuatrimestre,
        )
    elif cuatrimestre == '1' or cuatrimestre == '2':
        comisiones_qs = comisiones_qs.filter(
            Q(cuatrimestre=0) | Q(cuatrimestre=cuatrimestre)
        )
    if especialidad:
        try:
            int(especialidad)
            comisiones_qs = comisiones_qs.filter(materia__especialidad__id=especialidad)
        except ValueError:
            pass
    if buscar and buscar != 'None':
        try:
            comisiones_qs = comisiones_qs.filter(
                Q(materia__nombre__icontains=buscar) | Q(comision__icontains=buscar)
            )
        except ValueError:
            pass

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="aulas.csv"'

    writer = csv.writer(response)

    fila = []

    fila.append('Detalle')
    fila.append('Especialidad')
    fila.append('Cantidad de inscriptos')
    for dia in DIAS_SEMANA_LIST:
        fila.append(dia.get('dia_nombre'))

    writer.writerow(fila)
    for comision in comisiones_qs:
        fila = []
        fila.append(comision.__str__())
        fila.append(comision.materia.especialidad.nombre)
        fila.append(comision.get_cantidad_inscriptos())
        for dia in DIAS_SEMANA_LIST:
            horarios = comision.get_horarios_comision_academico()
            horario = get_horario(horarios, dia.get('dia'))
            if horario:
                fila.append("{0!s} a {1!s}".format(horario.get('hora_inicio'), horario.get('hora_fin')))
            else:
                fila.append("")

        writer.writerow(fila)
    return response
