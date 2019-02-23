from django import forms

from app_academica.models.comision import SEMESTRE, Comision
from app_academica.models import Especialidad
from app_academica.utils import obtener_anio_academico


class FilterComisionForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(FilterComisionForm, self).__init__(*args, **kwargs)

        comision_qs = Comision.objects.order_by().values('anioacademico').distinct()

        initial = None
        if comision_qs:

            initial = obtener_anio_academico()

            if not comision_qs.filter(anioacademico=initial):

                initial = comision_qs.first().get('anioacademico')


        self.fields['anioacademico'] = forms.ChoiceField(
            choices=[('', '---------')] + [(comision.get('anioacademico'), comision.get('anioacademico')) for comision in comision_qs],
            widget=forms.Select(attrs={'class': 'form-control'}),
            initial=initial
        )

    semestre = forms.ChoiceField(
                choices=[('', '---------')] + sorted(SEMESTRE.items()),
                widget=forms.Select(attrs={'id': 'semestre_select', 'class': 'form-control'})
            )

    especialidad = forms.ModelChoiceField(
        queryset=Especialidad.objects.filter(visible=True),
        widget=forms.Select(attrs={'id': 'especialidad_select', 'class': 'form-control'})
    )

    buscar = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'especialidad_select', 'class': 'form-control'})
    )

    anioacademico = forms.CharField(
        widget=forms.Select(attrs={'id': 'anioacademico_select', 'class': 'form-control'})
    )
