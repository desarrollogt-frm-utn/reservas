# -*- encoding:utf-8 -*-
from django import forms

from ..models import Recurso


class RecursoForm(forms.ModelForm):
    class Meta:
        model = Recurso
        fields = [
            'nombre',
            'observaciones',
            'tipo_recurso',
            'nro_incidente',
        ]
        labels = {
            'nombre': 'ID del equipo',
            'observaciones': 'Observaciones',
            'tipo_recurso': 'Tipo de Recurso',
            'nro_incidente': 'N° de Incidente',

        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control'}),
            'tipo_recurso': forms.Select(attrs={'class': 'form-control'}),
            'nro_incidente': forms.NumberInput(attrs={'class': 'form-control'})
        }
