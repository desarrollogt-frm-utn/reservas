from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView
from django.conf import settings


from app_reservas.models import (
    Solicitud,
    HistoricoEstadoSolicitud,
    Reserva,
)
from app_reservas.form import (
    ReservaCreateForm,
    FilterReservaForm
)

from app_reservas.form.reserva import ReservaInlineFormset

from app_usuarios.models import Docente as DocenteModel


def ReservaCreate(request):
    solicitud = Solicitud()
    reserva_form = ReservaCreateForm()  # setup a form for the parent
    formset = ReservaInlineFormset(instance=solicitud)

    if request.method == "POST":
        reserva_form = ReservaCreateForm(request.POST)

        formset = ReservaInlineFormset(request.POST, request.FILES)

        if reserva_form.is_valid():
            formset = ReservaInlineFormset(request.POST, request.FILES)

            if formset.is_valid():
                docente_obj = reserva_form.cleaned_data.get('docente')
                docente_model_qs = DocenteModel.objects.filter(legajo=docente_obj.legajo)[:1]
                docente_model = None
                if docente_model_qs:
                    docente_model = docente_model_qs[0]
                comision_obj = None
                if reserva_form.cleaned_data.get('comision'):
                    comision_obj = reserva_form.cleaned_data.get('comision')
                solicitud_obj = Solicitud.objects.create(
                    fechaCreacion=timezone.now(),
                    tipoSolicitud=reserva_form.cleaned_data.get('tipoSolicitud'),
                    docente=docente_obj,
                    comision=comision_obj,
                    fechaInicio=reserva_form.cleaned_data.get('fechaInicio'),
                    fechaFin=reserva_form.cleaned_data.get('fechaFin'),
                    solicitante=docente_model,
                )
                HistoricoEstadoSolicitud.objects.create(
                    fechaInicio=timezone.now(),
                    fechaFin=None,
                    estadoSolicitud=1,
                    solicitud=solicitud_obj,
                )
                formset = ReservaInlineFormset(request.POST, request.FILES, instance=solicitud_obj)
                for horario in formset.forms:
                    horario.save()
                return render(request, 'app_reservas/solicitud_created.html', {})
    return render(request, 'app_reservas/reserva_create.html', {
        "form": reserva_form,
        "formset": formset,
    })


class ReservaList(ListView):
    model = Reserva
    template_name = 'app_reservas/reservas_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ReservaList, self).get_context_data(**kwargs)
        estado = FilterReservaForm(self.request.GET)
        context['estado'] = estado
        return context

    def get_queryset(self):
        filter_val = self.request.GET.get('estado', '')
        order = self.request.GET.get('orderby', '')
        reservas_qs = Reserva.objects.all()
        if filter_val:
            reservas_qs = reservas_qs.filter(
                historicoestadosolicitud__estadoSolicitud__id=filter_val,
                historicoestadosolicitud__fechaFin__isnull=True,
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
                historicoestadosolicitud__estadoSolicitud__id=filter_val,
                historicoestadosolicitud__fechaFin__isnull=True,
            )
        return reservas_qs
