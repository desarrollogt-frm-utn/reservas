# coding=utf-8
import csv
import codecs
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.views.generic.list import ListView

from app_academica.adapters.frm_utn import get_horarios
from app_academica.form import FilterComisionForm
from app_academica.models import Especialidad, Materia, Comision
from app_academica.models.comision import SEMESTRE
from app_academica.constants import DIAS_SEMANA_LIST
from app_academica.services.serializerService import get_docentes_by_comision_materia_especialidad_plan
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
            'semestre': horario['cuatrimest']
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
        context['semestre'] = SEMESTRE
        context['dias_semana'] = DIAS_SEMANA_LIST
        context['horarios'] = get_horarios()
        return context

    def get_queryset(self):
        especialidad = self.request.GET.get('especialidad', '')
        semestre = self.request.GET.get('semestre', '')
        buscar = self.request.GET.get('buscar','')
        comisiones_qs = Comision.objects.filter(materia__especialidad__visible=True)
        if semestre == '0':
          comisiones_qs = comisiones_qs.filter(
                semestre=semestre,
            )
        elif semestre == '1' or semestre == '2':
            comisiones_qs = comisiones_qs.filter(
                Q(semestre=0) | Q(semestre=semestre)
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
    semestre = request.GET.get('semestre', '')
    buscar = request.GET.get('buscar', '')
    comisiones_qs = Comision.objects.filter(materia__especialidad__visible=True)
    if semestre == '0':
        comisiones_qs = comisiones_qs.filter(
            semestre=semestre,
        )
    elif semestre == '1' or semestre == '2':
        comisiones_qs = comisiones_qs.filter(
            Q(semestre=0) | Q(semestre=semestre)
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

    response.write(codecs.BOM_UTF8)
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


class ComisionDetailView(DetailView):
    """
    Vista de detalle para una instancia específica de Comision.
    """
    model = Comision
    context_object_name = 'comision'
    template_name = 'app_reservas/comision_detail.html'

    def get_object(self, **kwargs):
        """
        Retorna la instancia de Comisión cuyo id concuerdan con
        el parámetros de la URL, o una respuesta 404 en caso
        de ser inválido.
        """
        return get_object_or_404(Comision, id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(ComisionDetailView, self).get_context_data(**kwargs)
        docente_list = get_docentes_by_comision_materia_especialidad_plan(
            self.object.codigo,
            self.object.materia.codigo,
            self.object.materia.especialidad.codigo,
            self.object.materia.plan.nombre
        )
        context['semestre'] = SEMESTRE
        context['dias_semana'] = DIAS_SEMANA_LIST
        context['docente_list'] = docente_list
        return context
