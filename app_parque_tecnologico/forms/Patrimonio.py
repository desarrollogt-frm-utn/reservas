# -*- encoding:utf-8 -*-
from django import forms

from ..models import Patrimonial


class PatrimonialForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PatrimonialForm, self).__init__(*args, **kwargs)

        self.fields['patrimonial_boolean'] = forms.BooleanField(
            label='Patrimonial',
            widget=forms.CheckboxInput(attrs={'checked': 'checked'})
        )

    class Meta:
        model = Patrimonial
        fields = [
            'id_patrimonial',
            'nro_expediente',
            'responsable'
        ]
        labels = {
            'id_patrimonial': 'ID patrimonial',
            'nro_expediente': 'Número de expediente',
            'responsable': 'Responsable'

        }
        widgets = {
            'id_patrimonial': forms.NumberInput(attrs={'class': 'form-control'}),
            'nro_expediente': forms.TextInput(attrs={'class': 'form-control'}),
            'responsable': forms.TextInput(attrs={'class': 'form-control'}),
        }
