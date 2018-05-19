from django import forms

from app_reservas.models.comision import CUATRIMESTRE
from app_reservas.models import Especialidad


class FilterComisionForm(forms.Form):
    cuatrimestre = forms.ChoiceField(
                choices=[('', '---------')] +sorted(CUATRIMESTRE.items()),
                widget=forms.Select(attrs={'id': 'cuatrimestre_select', 'class': 'form-control'})
            )

    especialidad = forms.ModelChoiceField(
        queryset=Especialidad.objects.filter(visible=True),
        widget=forms.Select(attrs={'id': 'especialidad_select', 'class': 'form-control'})
    )

    buscar = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'especialidad_select', 'class': 'form-control'})
    )
