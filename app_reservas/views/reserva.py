import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.conf import settings
from rolepermissions.decorators import has_permission_decorator

from app_reservas.adapters.google_calendar import obtener_evento_especifico
from app_reservas.errors import not_found_error, custom_error
from app_reservas.models import (
    Solicitud,
    HorarioReserva,
    HistoricoEstadoReserva,
    Reserva,
)
from app_reservas.form import (
    ReservaCreateForm,
    FilterReservaForm
)
from app_reservas.models.historicoEstadoReserva import ESTADO_RESERVA, ESTADOS_FINALES
from app_reservas.models.horarioReserva import DIAS_SEMANA
from app_reservas.roles import CREATE_RESERVA
from app_reservas.services.recursos import get_recurso_obj
from app_reservas.services.reservas import crear_evento, dar_baja_evento
from app_reservas.form.reserva import ReservaInlineFormset

from app_usuarios.models import Usuario as UsarioModel


@has_permission_decorator(CREATE_RESERVA)
def reservaCreate(request):
    solicitud = Solicitud()
    reserva_form = ReservaCreateForm()  # setup a form for the parent
    formset = ReservaInlineFormset(instance=solicitud, request=request)

    if request.method == "POST":
        reserva_form = ReservaCreateForm(request.POST)

        formset = ReservaInlineFormset(request.POST, request.FILES, request=request)

        if reserva_form.is_valid():
            if formset.is_valid():
                docente_obj = reserva_form.cleaned_data.get('docente')
                usuario_model_qs = UsarioModel.objects.filter(legajo=docente_obj.legajo)[:1]
                usuario_model = None
                if usuario_model_qs:
                    usuario_model = usuario_model_qs[0]
                comision_obj = None
                if reserva_form.cleaned_data.get('comision'):
                    comision_obj = reserva_form.cleaned_data.get('comision')
                nombre_evento = reserva_form.cleaned_data.get('nombre_evento')
                fecha_inicio = reserva_form.cleaned_data.get('fecha_inicio')
                fecha_fin = reserva_form.cleaned_data.get('fecha_fin')

                created_reservas = []

                for reserva in formset.forms:
                    recurso_obj = reserva.cleaned_data.get('recurso')
                    reserva_obj = None
                    for created_reserva in created_reservas:
                        if created_reserva.recurso == recurso_obj:
                            reserva_obj = created_reserva

                    if not reserva_obj:
                        reserva_obj = Reserva.objects.create(
                            fecha_creacion=timezone.now(),
                            fecha_inicio=fecha_inicio,
                            fecha_fin=fecha_fin,
                            nombre_evento=nombre_evento,
                            asignado_por=request.user,
                            recurso=recurso_obj,
                            docente=docente_obj,
                            comision=comision_obj,
                            usuario=usuario_model
                        )
                        HistoricoEstadoReserva.objects.create(
                            fecha_inicio=timezone.now(),
                            estado='1',
                            reserva=reserva_obj,
                        )
                        created_reservas.append(reserva_obj)

                    HorarioReserva.objects.create(
                        reserva=reserva_obj,
                        dia=reserva.cleaned_data.get('dia'),
                        inicio=reserva.cleaned_data.get('inicio'),
                        fin=reserva.cleaned_data.get('fin'),
                    )
                for created_reserva in created_reservas:
                    crear_evento(created_reserva)

                return render(request, 'commons/success_message.html', {
                    'title': 'Se registro tu reserva',
                    'message': 'Tu reserva se ha registrado con éxito.'
                })
    return render(request, 'app_reservas/reserva_create.html', {
        "form": reserva_form,
        "formset": formset,
        "SITE_URL": settings.SITE_URL
    })


@has_permission_decorator(CREATE_RESERVA)
def ReservaFinalize(request, pk):
    reserva_qs = Reserva.objects.filter(id=pk)[:1]
    if not reserva_qs:
        return not_found_error(request)
    reserva_obj = reserva_qs[0]
    estado_antiguo = reserva_obj.get_estado_reserva()
    if estado_antiguo and estado_antiguo.estado in ESTADOS_FINALES:
        return custom_error(request, 'La reserva ya se encuentra finalizado o dada de baja.')
    if request.method == "POST":
        dar_baja_evento(reserva_obj)

        return render(request, 'commons/success_message.html', {
            'title': 'La reserva fue finalizada',
            'message': 'La reserva ha sido finalizada con éxito.'
        })
    return render(request, 'app_reservas/reserva_delete.html', {
        "reserva_obj": reserva_obj,
        "dias_semana": DIAS_SEMANA
    })


class ReservaDetail(DetailView):
    """
    Vista de detalle para una instancia específica de una Reserva.
    """
    model = Reserva
    context_object_name = 'reserva'
    template_name = 'app_reservas/reserva_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ReservaDetail, self).get_context_data(**kwargs)
        estado_reserva_context = context['reserva'].get_estado_reserva()
        estado_reserva_context.estado_nombre = ESTADO_RESERVA.get(estado_reserva_context.estado)
        estado_reserva_context.estado_final = estado_reserva_context and estado_reserva_context.estado in ESTADOS_FINALES
        context['estado_reserva'] = estado_reserva_context
        context["dias_semana"] = DIAS_SEMANA
        return context


class ReservaList(ListView):
    model = Reserva
    template_name = 'app_reservas/reservas_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ReservaList, self).get_context_data(**kwargs)
        estado_form = FilterReservaForm(self.request.GET)
        context['estado_form'] = estado_form
        context['estado_reserva'] = ESTADO_RESERVA
        return context

    def get_queryset(self):
        estado = self.request.GET.get('estado', '')
        order = self.request.GET.get('orderby', '')
        reservas_qs = Reserva.objects.all().order_by('-id')
        if not estado:
            estado = '1'
        reservas_qs = reservas_qs.filter(
            historicoestadoreserva__estado=estado,
            historicoestadoreserva__fecha_fin__isnull=True,
        )
        return reservas_qs


class ReservaListDocente(ListView):
    model = Reserva
    template_name = 'app_reservas/reservas_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ReservaListDocente, self).get_context_data(**kwargs)
        estado = FilterReservaForm(self.request.GET)
        context['estado'] = estado
        return context

    def get_queryset(self):
        filter_val = self.request.GET.get('estado', '')
        order = self.request.GET.get('orderby', '')
        reservas_qs = Reserva.objects.filter(docente__id=self.request.user.id)
        if filter_val:
            reservas_qs = reservas_qs.filter(
                historicoestadosolicitud__estado_solicitud__id=filter_val,
                historicoestadosolicitud__fecha_fin__isnull=True,
            )
        return reservas_qs


def reserva_eventos_json(request, pk):
    """
    Retorna en formato JSON una lista de los eventos para una instancia específica de Reserva (cuyo
    ID está dado por el parámetro 'pk').

    Si se especifican los parámetros GET 'start' y 'end' (ambos con formatos de fecha válidos), los
    eventos a retornar quedan conformados sólo por aquellos cuya fecha de inicio está contenida en
    el período especificado.
    """
    reserva = get_object_or_404(Reserva, pk=pk)
    eventos = []
    recurso_obj = get_recurso_obj(reserva.recurso.id)
    if recurso_obj:
        for horario_reserva in reserva.horarioreserva_set.all():
            eventos += obtener_evento_especifico(
                recurso_obj.calendar_codigo,
                horario_reserva.id_evento_calendar
            )

    from app_reservas.utils import parse_eventos_response

    parsed_events = parse_eventos_response(eventos, pk)

    return JsonResponse(json.loads(parsed_events), safe=False)
