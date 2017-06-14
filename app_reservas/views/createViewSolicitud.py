from django.shortcuts import render
from django.http import HttpResponseRedirect
from ..models import Solicitud
from ..form import SolicitudInlineFormset, SolicitudForm


def SolicitudCreate(request):
    solicitud = Solicitud()
    solicitud_form = SolicitudForm()  # setup a form for the parent
    formset = SolicitudInlineFormset(instance=solicitud)

    if request.method == "POST":
        solicitud_form = SolicitudInlineFormset(request.POST)

        if id:
            solicitud_form = SolicitudInlineFormset(request.POST, instance=solicitud)

        formset = SolicitudInlineFormset(request.POST, request.FILES)

        if solicitud_form.is_valid():
            created_solicitud = solicitud_form.save(commit=False)
            formset = SolicitudInlineFormset(request.POST, request.FILES, instance=created_solicitud)

            if formset.is_valid():
                created_solicitud.save()
                formset.save()
                return HttpResponseRedirect(created_solicitud.get_absolute_url())

    return render(request, 'app_reservas/solicitud_material.html', {
        "form": solicitud_form,
        "formset": formset,
    })
