import time
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from ..models import Recurso, Trazabilidad
from ..forms import RecursoForm, ComponenteForm, PatrimonialForm, TrazabilidadForm


# Create your views here.


class RecursoCreate(CreateView):
    model = Recurso
    template_name = 'app_parque_tecnologico/recurso_create.html'
    form_class = RecursoForm
    second_form_class = ComponenteForm
    third_form_class = PatrimonialForm
    forth_form_class = TrazabilidadForm
    success_url = reverse_lazy('adopcion:solicitud_listar')

    def get_context_data(self, **kwargs):
        context = super(RecursoCreate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'componente' not in context:
            context['componente'] = self.second_form_class(self.request.GET)
        if 'patrimonial' not in context:
            context['patrimonial'] = self.third_form_class(self.request.GET)
        if 'trazabilidad' not in context:
            context['trazabilidad'] = self.forth_form_class(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        current_user = request.user
        recurso = self.form_class(request.POST)
        print(time.strftime("%Y-%m-%d %H:%M"))
        componente = self.second_form_class(request.POST)
        trazabilidad = self.forth_form_class(request.POST)
        if recurso.is_valid():
            recurso_obj = recurso.save(commit=False)
            recurso_obj.autor = current_user
            recurso_obj.fecha_alta = time.strftime("%Y-%m-%d %H:%M")
            if request.POST.get("patrimonial_boolean",""):
                patrimonial = self.third_form_class(request.POST)
                if patrimonial.is_valid():
                    recurso_obj.patrimonial = patrimonial.save()
            if trazabilidad.is_valid():
                rec = recurso_obj.save()
                trazabilidad_obj = trazabilidad.save(commit=False)
                trazabilidad_obj.fechaInicio = time.strftime("%Y-%m-%d %H:%M")


        if form.is_valid() and componente.is_valid():
            solicitud = form.save(commit=False)
            solicitud.persona = componente.save()
            solicitud.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, componente=componente))