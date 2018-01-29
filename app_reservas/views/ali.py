# coding=utf-8
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView

from django.conf import settings

from rolepermissions.decorators import has_role_decorator

from app_reservas.form import ElementoForm
from app_reservas.errors import not_found_error, custom_error
from app_reservas.tasks import crear_evento_recurso_especifico
from app_reservas.utils import obtener_siguiente_dia_vigente

from app_usuarios.models import Docente as DocenteModel

from ..models import (
    Aula,
    Accesorio,
    AccesorioPrestamo,
    CarruselImagenes,
    HorarioReserva,
    LaboratorioInformatico,
    Prestamo,
    Recurso,
    RecursoPrestamo,
    Reserva,
    TipoRecursoAli,
)
from app_reservas.form import (
    AliRecursoForm,
    PrestamoReservaForm,
    ReservaCreateForm,
    ReservaWithoutSolicitudCreateForm
)


class AliTemplateView(TemplateView):
    """
    Vista de plantilla para la página principal del ALI.
    """
    template_name = 'app_reservas/ali_index.html'

    def get_context_data(self, **kwargs):
        """
        Añade al contexto el carrusel de imágenes del index.
        """
        # Obtiene la información de contexto base.
        context = super(AliTemplateView, self).get_context_data(**kwargs)

        # Añade el carrusel de imágenes de la página del ALI, en caso de que exista.
        try:
            carrusel = CarruselImagenes.objects.get(slug='ali_index')

            context['carrusel'] = carrusel
            context['carrusel_imagenes'] = carrusel.imagenes.all()
        except ObjectDoesNotExist:
            pass

        # Añade los tipos de recurso del ALI existentes.
        context['tipos_recurso_ali'] = TipoRecursoAli.objects.all()

        # Añade la cantidad de laboratorios de Informática existentes.
        context['cantidad_laboratorios_informatica'] = LaboratorioInformatico.objects.all().count()

        # Retorna el contexto modificado.
        return context


class AliVideoconferenciasDetailView(DetailView):
    """
    Vista de detalle para la sala de videoconferencias del ALI.
    """
    model = Aula
    context_object_name = 'aula'

    def get_object(self):
        # Obtiene la instancia de la sala de videoconferencias.
        return Aula.objects.filter(
            nivel__cuerpo__numero=6,
            nivel__numero=2,
            numero=1,
        ).first()


@has_role_decorator('administrador')
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
                request.session['recurso_list'] = [recurso_obj.id]
                request.session['accesorio_list'] = []
                request.session['recursos_tuple'] = []
                return redirect(reverse_lazy('prestamo_crear'))
    return render(request, 'app_reservas/prestamo_register.html', {
        'form': form,
    })


@has_role_decorator('administrador')
def PrestamoCreate(request):
    recurso_list = request.session.get('recurso_list', [])
    accesorio_list = request.session.get('accesorio_list', [])
    recursos = []
    accesorios = []
    for i, recurso in enumerate(recurso_list):
        recurso_qs = Recurso.objects.filter(id=recurso)[:1]
        if recurso_qs:
            prefix = 'recurso-{0:d}'.format(i)
            form = PrestamoReservaForm(request, recurso_qs[0], prefix=prefix)
            recursos.append({
                'object': recurso_qs[0],
                'form': form
                })
        else:
            return not_found_error()
    for accesorio in accesorio_list:
        accesorio_qs = Accesorio.objects.filter(id=accesorio)[:1]
        if accesorio_qs:
            accesorios.append(accesorio_qs[0])
        else:
            return not_found_error()

    if request.method == "POST":
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
        'accesorios': accesorios
    })


@has_role_decorator('administrador')
def PrestamoElementAdd(request):
    form = ElementoForm(request)
    if request.method == "POST":
        form = ElementoForm(request, request.POST)
        if form.is_valid():
            recurso_list = request.session.get('recurso_list', [])
            accesorio_list = request.session.get('accesorio_list',[])
            elemento_obj = form.cleaned_data['recurso']
            if type(elemento_obj) is Accesorio:
                accesorio_list.append(elemento_obj.id)
            else:
                recurso_list.append(elemento_obj.id)
            request.session['recurso_list'] = recurso_list
            request.session['accesorio_list'] = accesorio_list
            return redirect(reverse_lazy('prestamo_crear'))
    return render(request, 'app_reservas/prestamo_add_element.html', {
        'form': form,
    })


@has_role_decorator('administrador')
def PrestamoElementsRemove(request):
    request.session['recurso_list'] = []
    request.session['accesorio_list'] = []
    request.session['recursos_tuple'] = []
    return redirect(reverse_lazy('prestamo_crear'))


@has_role_decorator('administrador')
def PrestamoConfirm(request):
    accesorio_list = request.session.get('accesorio_list', [])
    recursos_tuple = request.session.get('recursos_tuple', [])
    show_form = False
    recursos = []
    accesorios = []
    for recurso in recursos_tuple:
        recurso_qs = Recurso.objects.filter(id=recurso.get('id', None))[:1]
        if recurso_qs:
            choice = recurso.get('choice', None)
            reserva_obj = None
            if not choice:
                show_form = True
            else:
                reserva_obj = Reserva.objects.get(id=choice)
            recursos.append({
                'object': recurso_qs[0],
                'reserva': reserva_obj
                })
        else:
            return not_found_error()
    for accesorio in accesorio_list:
        accesorio_qs = Accesorio.objects.filter(id=accesorio)[:1]
        if accesorio_qs:
            accesorios.append(accesorio_qs[0])
        else:
            return not_found_error()
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
                    reserva_form.pop('tipoSolicitud')
                    docente_obj = reserva_form.pop('docente')
                    try:
                        docente_model_obj = DocenteModel.objects.get(legajo=docente_obj.legajo)
                    except DocenteModel.DoesNotExist:
                        docente_model_obj = None
                    reserva_obj = Reserva(docente=docente_model_obj, **reserva_form)
                    reserva_obj.asignado_por = request.user
                    reserva_obj.recurso = recurso.get('object')
                    reserva_obj.save()
                    HorarioReserva.objects.create(
                        inicio=timezone.now(),
                        fin=timezone.now(),
                        reserva=reserva_obj,
                        dia=timezone.localtime(timezone.now()).weekday()+1
                    )
                    fin = timezone.now() + timezone.timedelta(hours=3)
                    crear_evento_recurso_especifico.delay(
                        calendar_id=recurso.get('object').calendar_codigo,
                        titulo=reserva_obj.nombreEvento,
                        inicio=timezone.now().isoformat(),
                        fin=fin.isoformat(),
                        hasta=None,
                    )
                else:
                    return render(request, 'app_reservas/prestamo_confirm.html', {
                        'form': form,
                        'recursos': recursos,
                        'accesorios': accesorios,
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
        prestamo_obj.save()
        for accesorio in accesorios:
            AccesorioPrestamo.objects.create(
                prestamo=prestamo_obj,
                accesorio=accesorio,
            )
        request.session['recurso_list'] = []
        request.session['accesorio_list'] = []
        request.session['recursos_tuple'] = []
        return redirect(reverse_lazy('prestamo_detalle', kwargs={'pk': prestamo_obj.id}))
    return render(request, 'app_reservas/prestamo_confirm.html', {
        'form': form,
        'recursos': recursos,
        'accesorios': accesorios,
        'SITE_URL': settings.SITE_URL
    })


@has_role_decorator('administrador')
def PrestamoFinalize(request, pk):
    prestamo_qs = Prestamo.objects.filter(id=pk)[:1]
    if not prestamo_qs:
        return not_found_error()
    prestamo_obj = prestamo_qs[0]
    if prestamo_obj.fin:
        return custom_error(request, 'El prestamo ya se encuentra en estado finalizado.')
    if request.method == 'POST':
        prestamo_obj.fin = timezone.now()
        prestamo_obj.recibido_por = request.user
        prestamo_obj.save()
        return redirect(reverse_lazy('prestamo_detalle', kwargs={'pk': pk}))
    return render(request, 'app_reservas/prestamo_finalize.html', {'prestamo_obj':prestamo_obj})


class PrestamoDetail(DetailView):
    template_name = 'app_reservas/prestamo_detail.html'
    model = Prestamo


class PrestamoList(ListView):
    model = Prestamo
    template_name = 'app_reservas/prestamo_list.html'
    paginate_by = 10
