# coding=utf-8

from django.utils import timezone
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView

from app_reservas.models import Comision, Docente, EstadoSolicitud, HistoricoEstadoSolicitud, Solicitud, TipoSolicitud
from app_reservas.models.horarioSolicitud import DIAS_SEMANA, TIPO_RECURSO
from app_reservas.form import FilterSolicitudForm, SolicitudInlineFormset, SolicitudForm

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
        solicitud_form = SolicitudInlineFormset(request.POST)

        formset = SolicitudInlineFormset(request.POST, request.FILES)

        if solicitud_form.is_valid():
            formset = SolicitudInlineFormset(request.POST, request.FILES)

            if formset.is_valid():
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

    return render(request, 'app_reservas/solicitud_material.html', {
        "form": solicitud_form,
        "formset": formset,
    })



class SolicitudList(ListView):
    model = Solicitud
    template_name = 'app_reservas/reservas_list.html'
    paginate_by = 20

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
