# coding=utf-8
from django.utils import timezone
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from django.conf import settings

from rolepermissions.decorators import has_permission_decorator

from app_reservas.form import ElementoForm
from app_reservas.errors import custom_error
from app_reservas.roles import FINALIZE_PRESTAMO, CREATE_PRESTAMO
from app_reservas.services.recursos import get_recurso_obj
from app_reservas.services.reservas import finalizar_reserva, crear_reserva_rapida, buscar_reservas
from app_reservas.utils import get_now_timezone

from ..models import (
    BaseRecurso,
    Prestamo,
    RecursoPrestamo,
    Reserva,
)
from app_reservas.form import (
    AliRecursoForm,
    PrestamoReservaForm,
    ReservaWithoutSolicitudCreateForm
)

PRESTAMO_FINALIZADO_MESSAGE = "El prestamo ya se encuentra en estado finalizado."
PRESTAMO_VACIO_MESSAGE = "Es necesario agregar al menos un recurso."
PRESTAMO_FUERA_DE_RANGO_MESSAGE = "El tiempo para agregar recursos expiró"
PRESTAMO_CON_RESERVA_MESSAGE = "El recurso no se encuentra disponible en el rango horario requerido"


@has_permission_decorator(CREATE_PRESTAMO)
def PrestamoRegister(request):
    form = AliRecursoForm()
    if request.method == "POST":
        form = AliRecursoForm(request.POST)
        if form.is_valid():
            recurso_obj = form.cleaned_data['recurso']
            # Compruebo si el recurso tiene reservas asociadas
            prestamo_obj = recurso_obj.get_active_loan()
            if prestamo_obj:
                return redirect(reverse_lazy('prestamo_detalle', kwargs={'pk': prestamo_obj.id}))
            else:
                recurso_list = [recurso_obj.id]
                request.session['recurso_list'] = recurso_list
                request.session['recursos_tuple'] = []
                return redirect(reverse_lazy('prestamo_crear'))
    return render(request, 'app_reservas/prestamo_register.html', {
        'form': form,
    })


@has_permission_decorator(CREATE_PRESTAMO)
def PrestamoCreate(request):
    recurso_list = request.session.get('recurso_list', [])
    recursos = []
    for i, recurso in enumerate(recurso_list):
        base_recurso_obj = get_object_or_404(BaseRecurso, id=recurso)
        prefix = 'recurso-{0:d}'.format(i)
        recurso_obj = get_recurso_obj(base_recurso_obj.id)
        form = None
        if recurso_obj:
            form = PrestamoReservaForm(request, recurso_obj, prefix=prefix)
        recursos.append({
            'object': base_recurso_obj,
            'form': form
            })
    if request.method == "POST":
        if not recurso_list:
            return custom_error(request, PRESTAMO_VACIO_MESSAGE)
        recursos_tuple = []
        for i, recurso in enumerate(recurso_list):
            prefix = 'recurso-{0:d}-reserva'.format(i)
            recursos_tuple.append({
                'id': recurso,
                'choice': request.POST.get(prefix)
                })
        request.session['recursos_tuple'] = recursos_tuple
        return redirect(reverse_lazy('prestamo_confirmar'))
    return render(request, 'app_reservas/prestamo_create.html', {
        'recursos': recursos,
    })


@has_permission_decorator(CREATE_PRESTAMO)
def PrestamoElementAddOnCreate(request):
    form = ElementoForm(request)
    if request.method == "POST":
        form = ElementoForm(request, request.POST)
        if form.is_valid():
            recurso_list = request.session.get('recurso_list', [])
            elemento_obj = form.cleaned_data['recurso']
            recurso_list.append(elemento_obj.id)
            request.session['recurso_list'] = recurso_list
            return redirect(reverse_lazy('prestamo_crear'))
    return render(request, 'app_reservas/prestamo_add_element.html', {
        'form': form,
    })

@has_permission_decorator(CREATE_PRESTAMO)
def PrestamoElementAdd(request, pk):
    prestamo_obj = get_object_or_404(Prestamo, pk=pk)
    if prestamo_obj.fin:
        return custom_error(request, PRESTAMO_FINALIZADO_MESSAGE)

    if get_now_timezone().date() > prestamo_obj.inicio.date():
        return custom_error(request, PRESTAMO_FUERA_DE_RANGO_MESSAGE)

    form = ElementoForm(request)
    if request.method == "POST":
        form = ElementoForm(request, request.POST)
        if form.is_valid():
            recurso_obj = form.cleaned_data['recurso']

            base_reserva = prestamo_obj.recursos_all.first().reserva

            from datetime import datetime

            horario_reserva = base_reserva.get_horario_de_fecha(datetime.now())

            if not horario_reserva:
                return custom_error(request, PRESTAMO_FUERA_DE_RANGO_MESSAGE)

            reserva_list = buscar_reservas(recurso_obj, datetime.now(), horario_reserva.inicio, horario_reserva.fin)

            if reserva_list:
                return custom_error(
                    request,
                    PRESTAMO_CON_RESERVA_MESSAGE.format(
                        reverse_lazy('reserva_detalle', kwargs={'pk': reserva_list[0].pk})
                    )
                )

            docente_obj = base_reserva.docente
            comision_obj = base_reserva.comision
            hora_fin = horario_reserva.fin

            reserva_obj = crear_reserva_rapida(
                recurso_obj,
                docente_obj,
                comision_obj,
                request.user,
                hora_fin
            )

            RecursoPrestamo.objects.create(
                recurso=recurso_obj,
                reserva=reserva_obj,
                prestamo=prestamo_obj
                )
            return redirect(reverse_lazy('prestamo_detalle', kwargs={'pk': pk}))
    return render(request, 'app_reservas/prestamo_add_element.html', {
        'form': form,
    })


@has_permission_decorator(CREATE_PRESTAMO)
def PrestamoElementsRemove(request):
    request.session['recurso_list'] = []
    request.session['recursos_tuple'] = []
    return redirect(reverse_lazy('prestamo_crear'))


@has_permission_decorator(CREATE_PRESTAMO)
def PrestamoConfirm(request):
    recursos_tuple = request.session.get('recursos_tuple', [])
    show_form = False
    recursos = []

    if not recursos_tuple:
        return custom_error(request, PRESTAMO_VACIO_MESSAGE)

    for recurso in recursos_tuple:
        recurso_obj = get_object_or_404(BaseRecurso, id=recurso.get('id', None))
        choice = recurso.get('choice', None)
        reserva_obj = None
        if not choice:
            show_form = True
        else:
            reserva_obj = Reserva.objects.get(id=choice)
        recursos.append({
            'object': recurso_obj,
            'reserva': reserva_obj
            })
    form = None
    if show_form:
        form = ReservaWithoutSolicitudCreateForm()
    if request.method == "POST":
        prestamo_obj = Prestamo(
            inicio=timezone.now(),
            fin=None,
            asignado_por=request.user,
        )
        for recurso in recursos:
            if show_form:
                form = ReservaWithoutSolicitudCreateForm(request.POST)
                if form.is_valid():
                    reserva_form = form.cleaned_data
                    docente_obj = reserva_form.pop('docente')
                    recurso_obj = recurso.get('object')
                    comision_obj = reserva_form.get('comision')
                    hora_fin = reserva_form.get('fin')

                    reserva_obj = crear_reserva_rapida(
                        recurso_obj,
                        docente_obj,
                        comision_obj,
                        request.user,
                        hora_fin
                    )
                else:
                    return render(request, 'app_reservas/prestamo_confirm.html', {
                        'form': form,
                        'recursos': recursos,
                        'SITE_URL': settings.SITE_URL
                    })
            else:
                reserva_obj = Reserva.objects.get(id=choice)
            prestamo_obj.save()
            RecursoPrestamo.objects.create(
                prestamo=prestamo_obj,
                recurso=recurso.get('object'),
                reserva=reserva_obj,
            )
        request.session['recurso_list'] = []
        request.session['recursos_tuple'] = []
        return redirect(reverse_lazy('prestamo_detalle', kwargs={'pk': prestamo_obj.id}))
    return render(request, 'app_reservas/prestamo_confirm.html', {
        'form': form,
        'recursos': recursos,
        'SITE_URL': settings.SITE_URL
    })


@has_permission_decorator(FINALIZE_PRESTAMO)
def PrestamoFinalize(request, pk):
    prestamo_obj = get_object_or_404(Prestamo, pk=pk)
    if prestamo_obj.fin:
        return custom_error(request, PRESTAMO_FINALIZADO_MESSAGE)
    if request.method == 'POST':
        prestamo_obj.fin = timezone.now()
        prestamo_obj.recibido_por = request.user
        prestamo_obj.save()
        for prestamo_reserva in prestamo_obj.recursos_all.all():
            if prestamo_reserva.reserva:
                finalizar_reserva(prestamo_reserva.reserva)
        return redirect(reverse_lazy('prestamo_detalle', kwargs={'pk': pk}))
    return render(request, 'app_reservas/prestamo_finalize.html', {'prestamo_obj':prestamo_obj})


class PrestamoDetail(DetailView):
    template_name = 'app_reservas/prestamo_detail.html'
    model = Prestamo


class PrestamoList(ListView):
    model = Prestamo
    template_name = 'app_reservas/prestamo_list.html'
    paginate_by = 10
    ordering = ['-id']