from ..forms.Incidente import IncidenteForm
from django.views.generic.edit import FormView

class IncidenteView(FormView):
    template_name = 'app_parque_tecnologico/incidente.html'
    form_class = IncidenteForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        incidente = self.request.POST.get("nro_incidente", "")
        print(incidente)
        form.send_email()
        return super(IncidenteView, self).form_valid(form)
