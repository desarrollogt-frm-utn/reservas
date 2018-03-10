# -*- encoding:utf-8 -*-
from django import forms

class IncidenteForm(forms.Form):
    nro_incidente = forms.CharField(
        label='N° de Incidente',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )