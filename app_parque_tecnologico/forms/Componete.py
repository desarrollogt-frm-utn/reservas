# -*- encoding:utf-8 -*-
from django import forms

from ..models import Componente


class ComponenteForm(forms.ModelForm):
    class Meta:
        model = Componente
        fields = [
            'capacidad',
            'modelo',
            'nro_serie',
            'MAC',
            'marca',
            'proveedor',
            'tipo_componente',
        ]
        labels = {
            'capacidad': 'Capacidad',
            'modelo': 'Modelo',
            'nro_serie': 'Número de serie',
            'MAC': 'MAC',
            'marca': 'Marca',
            'proveedor': 'Proveedor',
            'tipo_componente': 'Tipo Componente',

        }
        widgets = {
            'capacidad': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'nro_serie': forms.TextInput(attrs={'class': 'form-control'}),
            'MAC': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.Select(attrs={'class': 'form-control'}),
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'tipo_componente': forms.Select(attrs={'class': 'form-control'}),
        }
