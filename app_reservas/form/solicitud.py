from django import forms
from django.forms import inlineformset_factory

from app_reservas.models import Solicitud, HorarioSolicitud, EstadoSolicitud, Comision


class SolicitudForm(forms.ModelForm):

    comision = forms.CharField(
        required=False,
        label='Comisión y Materia:',
        widget=forms.Select(attrs={'id': 'mat_select', 'class': 'form-control', 'disabled': 'true'}),
    )

    class Meta:
        model = Solicitud
        fields = ['docente', 'tipoSolicitud', 'comision']
        widgets = {
            'docente': forms.Select(attrs={'id': 'docente_select', 'class': 'form-control'}),
            'tipoSolicitud': forms.Select(attrs={'id': 'tipo_select', 'class': 'form-control', 'disabled': 'true'}),
        }

    def clean_comision(self):
        comision = self.cleaned_data['comision']
        tipo_solicitud = self.cleaned_data['tipoSolicitud']
        if tipo_solicitud.nombre == 'Cursado':
            if not comision:
                raise forms.ValidationError("La comision no puede estar vacia")
        comision_obj = Comision.objects.get(id=comision)
        return comision_obj


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

    def clean_fin(self):
        inicio = self.cleaned_data['inicio']
        fin = self.cleaned_data['fin']
        if not fin:
            raise forms.ValidationError(
                "La hora de inicio no puede ser nula"
            )
        if inicio > fin:
            raise forms.ValidationError(
                "La hora de fin de la solicitud no puede ser menor a la hora de inicio"
            )
        return fin

    def clean_incio(self):
        inicio = self.cleaned_data['inicio']
        if not inicio:
            raise forms.ValidationError(
                "La hora de inicio no puede ser nula"
            )
        return inicio




SolicitudInlineFormset = inlineformset_factory(Solicitud, HorarioSolicitud, form=HorarioSolicitudForm, extra=3)

class FilterSolicitudForm(forms.Form):
    estado = forms.ChoiceField(
                choices=[('', 'Todos')] +
                [(estado.id, estado.nombre) for estado in EstadoSolicitud.objects.all()],
                widget=forms.Select(attrs={'id': 'estado_select', 'class': 'form-control'})
            )
