from django import forms
from django.forms import inlineformset_factory

from app_reservas.models import Solicitud, HorarioSolicitud


class SolicitudForm(forms.ModelForm):

    materia = forms.ChoiceField(
        label='Comisión y Materia:',
        widget=forms.Select(attrs={'id': 'mat_select', 'class': 'form-control', 'disabled': 'true'}),
    )

    class Meta:
        model = Solicitud
        fields = ['docente', 'tipoSolicitud', 'materia' ]
        widgets = {
            'docente': forms.Select(attrs={'id': 'docente_select', 'class': 'form-control'}),
            'tipoSolicitud': forms.Select(attrs={'id': 'tipo_select', 'class': 'form-control', 'disabled': 'true'}),
        }


class HorarioSolicitudForm(forms.ModelForm):

    class Meta:
        model = HorarioSolicitud
        fields = ['dia', 'tipoRecurso', 'inicio', 'fin', 'cantidad_alumnos', 'softwareRequerido', 'tipoLaboratorio', 'tipoRecursoAli']
        widgets = {
            'dia': forms.Select(attrs={'class': 'form-control', }),
            'inicio': forms.TimeInput(
                attrs={'class': 'form-control', }
            ),
            'fin': forms.TimeInput(
                format='%h:%M %p',
                attrs={'class': 'form-control', }
            ),
            'cantidad_alumnos': forms.TextInput(
                attrs={'class': 'form-control', }
            ),
            'tipoRecurso': forms.Select(attrs={'class': 'form-control', }),
            'tipoLaboratorio': forms.Select(attrs={'class': 'form-control', 'disabled': 'true'}),
            'tipoRecursoAli': forms.SelectMultiple(attrs={'class': 'form-control', 'disabled': 'true'}),
        }


SolicitudInlineFormset = inlineformset_factory(Solicitud, HorarioSolicitud, form=HorarioSolicitudForm, extra=2)
