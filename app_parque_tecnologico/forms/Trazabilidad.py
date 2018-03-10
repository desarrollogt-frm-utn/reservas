# -*- encoding:utf-8 -*-
from django import forms

from ..models import Trazabilidad
from app_reservas.models import Cuerpo


class TrazabilidadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TrazabilidadForm, self).__init__(*args, **kwargs)

        cuerpo_qs = Cuerpo.objects.all()
        self.fields['local'] = forms.ChoiceField(
            choices=[('0', '---------')],
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        self.fields['cuerpo'] = forms.ChoiceField(
            choices=[('', '---------')] +[(cuerpo.id, cuerpo.nombre) for cuerpo in cuerpo_qs],
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        self.fields['nivel'] = forms.ChoiceField(
            choices=[('0', '---------')],
            widget=forms.Select(attrs={'class': 'form-control'})
        )

    class Meta:
        model = Trazabilidad
        fields = [
            'seccion',
        ]
        labels = {
            'seccion': 'Sección',

        }
        widgets = {
            'seccion': forms.Select(attrs={'class': 'form-control'}),
        }
