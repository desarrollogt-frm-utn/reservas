# coding=utf-8
import datetime

from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse_lazy

from django.conf import settings


from rolepermissions.decorators import has_role_decorator
from rolepermissions.checkers import has_permission


from app_reservas.errors import not_found_error

from app_reservas.models import (
    Aula,
    HistoricoEstadoSolicitud,
    HistoricoEstadoReserva,
    HorarioSolicitud,
    HorarioReserva,
    Laboratorio,
    LaboratorioInformatico,
    Recurso,
    RecursoAli,
    Reserva,
    Solicitud,
    )
from app_reservas.models.horarioSolicitud import DIAS_SEMANA, TIPO_RECURSO
from app_reservas.models.solicitud import TIPO_SOLICITUD
from app_reservas.form import FilterSolicitudForm, ReservaAssignForm, SolicitudInlineFormset, SolicitudForm
from app_reservas.services.reservas import crear_evento, get_nombre_evento
from app_academica.models import Docente

from app_usuarios.models import Usuario as UsuarioModel

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
    usuario_model = get_object_or_404(UsuarioModel, pk=request.user.id)
    solicitud = Solicitud()
    solicitud_form = SolicitudForm(request)  # setup a form for the parent
    formset = SolicitudInlineFormset(instance=solicitud)

    if request.method == "POST":
        solicitud_form = SolicitudForm(request, request.POST)

        formset = SolicitudInlineFormset(request.POST, request.FILES)

        if solicitud_form.is_valid():
            formset = SolicitudInlineFormset(request.POST, request.FILES)

            if formset.is_valid():
                docente_obj = Docente.objects.get(legajo=usuario_model.legajo)
                comision_obj = None
                if solicitud_form.cleaned_data.get('comision'):
                    comision_obj = solicitud_form.cleaned_data.get('comision')
                solicitud_obj = Solicitud.objects.create(
                    fecha_creacion=timezone.now(),
                    tipo_solicitud=solicitud_form.cleaned_data.get('tipo_solicitud'),
                    docente=docente_obj,
                    comision=comision_obj,
                    fecha_inicio=solicitud_form.cleaned_data.get('fecha_inicio'),
                    fecha_fin=solicitud_form.cleaned_data.get('fecha_fin'),
                    solicitante=usuario_model,
                )
                HistoricoEstadoSolicitud.objects.create(
                    fecha_inicio=timezone.now(),
                    fecha_fin=None,
                    estado_solicitud=1,
                    solicitud=solicitud_obj,
                )
                formset = SolicitudInlineFormset(request.POST, request.FILES, instance=solicitud_obj)
                for horario in formset.forms:
                    horario.save()
                return render(request, 'app_reservas/solicitud_created.html', {})
    return render(request, 'app_reservas/solicitud_material.html', {
        "form": solicitud_form,
        "formset": formset,
        "SITE_URL": settings.SITE_URL
    })



class SolicitudList(ListView):
    model = Solicitud
    template_name = 'app_reservas/solicitud_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(SolicitudList, self).get_context_data(**kwargs)
        estado = FilterSolicitudForm(self.request.GET)
        context['estado'] = estado
        context['tipos_solicitudes'] = TIPO_SOLICITUD
        return context

    def get_queryset(self):
        filter_val = self.request.GET.get('estado', '')
        order = self.request.GET.get('orderby', '')
        user = self.request.user
        solicitudes_qs = Solicitud.objects.all()
        if not has_permission(user, 'edit_reserva_estado'):
            usuario = UsuarioModel.objects.get(id=user.id)
            solicitudes_qs = solicitudes_qs.filter(solicitante=usuario)
        if filter_val:
            solicitudes_qs = solicitudes_qs.filter(
                historicoestadosolicitud__estado_solicitud__id=filter_val,
                historicoestadosolicitud__fecha_fin__isnull=True,
            )
        return solicitudes_qs


class SolicitudDetail(DetailView):
    template_name = 'app_reservas/solicitud_detail.html'
    model = Solicitud

    def get_context_data(self, **kwargs):
            context = super(SolicitudDetail, self).get_context_data(**kwargs)
            context['dias_semana'] = DIAS_SEMANA
            context['tipo_recursos'] = TIPO_RECURSO
            context['tipos_solicitudes'] = TIPO_SOLICITUD
            return context

    def get_template_names(self):
        user = self.request.user
        solicitud_obj = self.object
        usuarios_list = UsuarioModel.objects.filter(id=user.id)[:1]
        if not (has_permission(user, 'edit_reserva_estado') or (usuarios_list and usuarios_list[0].legajo == solicitud_obj.docente.legajo)):
            return not_found_error(self.request)

        else:
            return [self.template_name]

@has_role_decorator('administrador')
def RecursoAssign(request, solicitud, horario):
    solicitud_obj = Solicitud.objects.get(id=solicitud)
    horario_obj = HorarioSolicitud.objects.get(id=horario)
    if horario_obj.tipo_recurso == '1':
        model = Aula
    elif horario_obj.tipo_recurso == '2':
        model = LaboratorioInformatico
    elif horario_obj.tipo_recurso == '3':
        model = Laboratorio
    elif horario_obj.tipo_recurso == '4':
        model = RecursoAli
    else:
        model = Recurso

    form = ReservaAssignForm(request, model)
    if request.method == "POST":
        form = ReservaAssignForm(request, model, request.POST)
        if form.is_valid():
            recurso_list = model.objects.filter(id=form.cleaned_data['recurso'])[:1]
            estado_solicitud = solicitud_obj.get_estado_solicitud
            if estado_solicitud.estado_solicitud.nombre == 'Pendiente':
                estado_solicitud.fecha_fin = timezone.now()
                estado_solicitud.save()
                HistoricoEstadoSolicitud.objects.create(
                    estado_solicitud=2,
                    solicitud=solicitud_obj,
                    fecha_inicio=timezone.now(),
                )

            titulo = get_nombre_evento(solicitud_obj.docente,solicitud_obj.comision)

            reserva_obj = Reserva.objects.create(
                asignado_por=request.user,
                fecha_creacion=timezone.now(),
                recurso=recurso_list[0],
                docente=solicitud_obj.solicitante,
                nombreEvento=titulo,
                fecha_inicio=solicitud_obj.fecha_inicio,
                fecha_fin=solicitud_obj.fecha_fin,
            )

            HorarioReserva.objects.create(
                reserva=reserva_obj,
                dia=horario_obj.dia,
                inicio=horario_obj.inicio,
                fin=horario_obj.fin,

            )

            HistoricoEstadoReserva.objects.create(
                fecha_inicio=timezone.now(),
                estado='1',
                reserva=reserva_obj,
            )

            crear_evento(reserva_obj)

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


def SolicitudReject(request, pk):
    solicitud_obj = get_object_or_404(Solicitud, pk=pk)
    user = request.user
    usuarios_list = UsuarioModel.objects.filter(id=user.id)[:1]

    if not (has_permission(user, 'edit_reserva_estado') or (usuarios_list and usuarios_list[0].legajo == solicitud_obj.docente.legajo)):
        return not_found_error(request)

    if request.method == 'POST':
        solicitud_obj.email = 'None'
        solicitud_obj.is_active = False
        solicitud_obj.save()
        return redirect(reverse_lazy('user_roles'))
    return render(request, 'app_reservas/solicitud_reject.html', {
            'solicitud_obj': solicitud_obj,
            'tipos_solicitudes': TIPO_SOLICITUD,
        })
