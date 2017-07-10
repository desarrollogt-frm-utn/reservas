# coding=utf-8
import datetime

from django.utils import timezone
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse_lazy

from rolepermissions.decorators import has_role_decorator

from app_reservas.adapters.google_calendar import crear_evento
from app_reservas.utils import obtener_siguiente_dia_vigente, obtener_fecha_finalizacion_reserva

from app_reservas.models import (
    Aula,
    Comision,
    Docente,
    EstadoSolicitud,
    HistoricoEstadoSolicitud,
    HorarioSolicitud,
    Laboratorio,
    LaboratorioInformatico,
    RecursoAli,
    Reserva,
    Solicitud,
    TipoSolicitud,
    )
from app_reservas.models.horarioSolicitud import DIAS_SEMANA, TIPO_RECURSO
from app_reservas.form import FilterSolicitudForm, ReservaAssignForm, SolicitudInlineFormset, SolicitudForm

from app_reservas.tasks import obtener_eventos_recurso_especifico, crear_evento_recurso_especifico

class SolicitudAliReclamosSugerencias(TemplateView):
    """
    Vista de plantilla para la página de reclamos y sugerencias del ALI.
    """
    template_name = 'app_reservas/solicitud_ali_reclamos_sugerencias.html'


class SolicitudAulaView(TemplateView):
    """
    Vista de plantilla para la página de solicitud de aula.
    """
    template_name = 'app_reservas/solicitud_aula.html'


class SolicitudInstalacionSoftwareView(TemplateView):
    """
    Vista de plantilla para la página de solicitud de instalación de software.
    """
    template_name = 'app_reservas/solicitud_instalacion_software.html'


class SolicitudLaboratorioInformaticoView(TemplateView):
    """
    Vista de plantilla para la página de solicitud de laboratorio informático.
    """
    template_name = 'app_reservas/solicitud_laboratorio_informatico.html'


class SolicitudMaterialMultimediaView(TemplateView):
    """
    Vista de plantilla para la página de solicitud de material multimedia.
    """
    template_name = 'app_reservas/solicitud_material_multimedia.html'

def SolicitudCreate(request):
    solicitud = Solicitud()
    solicitud_form = SolicitudForm()  # setup a form for the parent
    formset = SolicitudInlineFormset(instance=solicitud)

    if request.method == "POST":
        solicitud_form = SolicitudForm(request.POST)

        formset = SolicitudInlineFormset(request.POST, request.FILES)

        if solicitud_form.is_valid():
            print('solicitud_form_valido')
            formset = SolicitudInlineFormset(request.POST, request.FILES)

            if formset.is_valid():
                print('formset_valido')
                docente_obj = Docente.objects.get(id=request.POST.get("docente"))
                tipo_solicitud_obj = TipoSolicitud.objects.get(id=request.POST.get("tipoSolicitud"))
                comision_obj = None
                if request.POST.get("comision"):
                    comision_obj = Comision.objects.get(id=request.POST.get("comision"))
                solicitud_obj = Solicitud.objects.create(
                    fechaCreacion=timezone.now(),
                    tipoSolicitud=tipo_solicitud_obj,
                    docente=docente_obj,
                    comision=comision_obj
                )
                estado = EstadoSolicitud.objects.get(nombre="Pendiente")
                HistoricoEstadoSolicitud.objects.create(
                    fechaInicio=timezone.now(),
                    fechaFin=None,
                    estadoSolicitud=estado,
                    solicitud=solicitud_obj,
                )
                formset = SolicitudInlineFormset(request.POST, request.FILES, instance=solicitud_obj)
                for horario in formset.forms:
                    horario.save()
                return render(request, 'app_reservas/solicitud_created.html', {})
        else:
            import ipdb; ipdb.set_trace()
            print('not_valid')
    return render(request, 'app_reservas/solicitud_material.html', {
        "form": solicitud_form,
        "formset": formset,
    })



class SolicitudList(ListView):
    model = Solicitud
    template_name = 'app_reservas/reservas_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(SolicitudList, self).get_context_data(**kwargs)
        estado = FilterSolicitudForm(self.request.GET)
        context['estado'] = estado
        return context

    def get_queryset(self):
        filter_val = self.request.GET.get('estado', '')
        order = self.request.GET.get('orderby', '')
        if filter_val:
            new_context = Solicitud.objects.filter(
                HistoricoEstadoSolicitud_set__estado__id=filter_val,
                historicosEstados__fechaFin__isnull=True,
            )
            return new_context
        return super(SolicitudList, self).get_queryset()


class SolicitudDetail(DetailView):
    template_name = 'app_reservas/reservas_detail.html'
    model = Solicitud

    def get_context_data(self, **kwargs):
            context = super(SolicitudDetail, self).get_context_data(**kwargs)
            context['dias_semana'] = DIAS_SEMANA
            context['tipo_recursos'] = TIPO_RECURSO
            return context

@has_role_decorator('administrador')
def RecursoAssign(request, solicitud, horario):
    solicitud_obj = Solicitud.objects.get(id=solicitud)
    horario_obj = HorarioSolicitud.objects.get(id=horario)
    if horario_obj.tipoRecurso == '1':
        model = Aula
    elif horario_obj.tipoRecurso == '2':
        model = LaboratorioInformatico
    elif horario_obj.tipoRecurso == '3':
        model = Laboratorio
    elif horario_obj.tipoRecurso == '4':
        model = RecursoAli

    form = ReservaAssignForm(request, model)
    if request.method == "POST":
        form = ReservaAssignForm(request, model, request.POST)
        if form.is_valid():
            recurso_list = model.objects.filter(id=form.cleaned_data['recurso'])[:1]
            estado_solicitud = solicitud_obj.get_estado_solicitud
            if estado_solicitud.estadoSolicitud.nombre == 'Pendiente':
                estado_solicitud.fechaFin = timezone.now()
                estado_solicitud.save()
                estado_en_curso_obj = EstadoSolicitud.objects.get(nombre='En curso')
                HistoricoEstadoSolicitud.objects.create(
                    estadoSolicitud=estado_en_curso_obj,
                    solicitud=solicitud_obj,
                    fechaInicio=timezone.now(),

                )

            Reserva.objects.create(
                asignado_por=request.user,
                fecha_creacion=timezone.now(),
                horario=horario_obj,
                recurso=recurso_list[0]
            )
            inicio = obtener_siguiente_dia_vigente(int(horario_obj.dia), horario_obj.inicio)
            fin = obtener_siguiente_dia_vigente(int(horario_obj.dia), horario_obj.fin)
            hasta = None
            if solicitud_obj.comision is not None:
                hasta = obtener_fecha_finalizacion_reserva(solicitud_obj.comision.cuatrimestre)
            if solicitud_obj.comision is not None:
                titulo = "{0!s} - {1!s}".format(solicitud_obj.comision.materia.nombre, solicitud_obj.docente.nombre)
            else:
                titulo = "Solicitud fuera de horario - {0!s}".format(solicitud_obj.docente.nombre)
            crear_evento_recurso_especifico.delay(
                calendar_id=recurso_list[0].calendar_codigo,
                titulo=titulo,
                inicio=inicio,
                fin=fin,
                hasta=hasta,
            )

            #
            # print(event)

            return redirect(reverse_lazy('solicitud_detalle', kwargs={'pk': solicitud_obj.id}))
    return render(request, 'app_reservas/recurso_assign.html', {
        'form': form,
        'object': solicitud_obj,
        'horario': horario_obj,
        'dias_semana': DIAS_SEMANA,
        'tipo_recursos': TIPO_RECURSO,
    })
