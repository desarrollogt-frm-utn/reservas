from django.shortcuts import render
from rolepermissions.decorators import has_role_decorator
from constance import config
from app_reservas.settings import FECHA_INICIO_PRIMER_SEMESTRE

from app_reservas.form import FechasSemestreForm

@has_role_decorator('administrador')
def FechasSemestreConfig(request):
    form = FechasSemestreForm(
        initial={
            'fecha_inicio_primer_semestre': config.FECHA_INICIO_PRIMER_SEMESTRE,
            'fecha_fin_primer_semestre': config.FECHA_FIN_PRIMER_SEMESTRE,
            'fecha_inicio_segundo_semestre': config.FECHA_INICIO_SEGUNDO_SEMESTRE,
            'fecha_fin_segundo_semestre': config.FECHA_FIN_SEGUNDO_SEMESTRE, }
    )

    if request.method == "POST":
        form = FechasSemestreForm(request.POST)

        if form.is_valid():
            config.FECHA_INICIO_PRIMER_SEMESTRE = form.cleaned_data['fecha_inicio_primer_semestre']
            config.FECHA_FIN_PRIMER_SEMESTRE = form.cleaned_data['fecha_fin_primer_semestre']
            config.FECHA_INICIO_SEGUNDO_SEMESTRE = form.cleaned_data['fecha_inicio_segundo_semestre']
            config.FECHA_FIN_SEGUNDO_SEMESTRE = form.cleaned_data['fecha_fin_segundo_semestre']
    return render(request, 'app_reservas/fechassemestre_config.html', {
        "form": form,
    })
