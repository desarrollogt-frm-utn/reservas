from django import forms
from django.forms import inlineformset_factory

from app_reservas.models import (
    Solicitud,
    HorarioSolicitud,
)

from app_academica.models import Comision
from app_reservas.utils import (
    obtener_fecha_inicio_reserva_cursado,
    obtener_fecha_fin_reserva_cursado,
)

from app_academica.adapters.frm_utn import get_comisiones_docentes
from app_usuarios.models import Usuario as UsuarioModel
from app_reservas.models.historicoEstadoSolicitud import ESTADO_SOLICITUD
from app_academica.utils import filter_by_legajo, obtener_anio_academico, obtener_comision_by_esp_mat_com_plan


class SolicitudForm(forms.ModelForm):

    def __init__(self, request=None, *args, **kwargs):
        super(SolicitudForm, self).__init__(*args, **kwargs)
        try:
            user = UsuarioModel.objects.get(id=request.user.id)
        except UsuarioModel.DoesNotExist:
            user = None

        docente_comisiones_qs = []
        if user:
            comisiones_list = get_comisiones_docentes(obtener_anio_academico())
            docente_comisiones_list = filter_by_legajo(comisiones_list, user.legajo)
            for comision_json in docente_comisiones_list:
                comision_obj = obtener_comision_by_esp_mat_com_plan(
                    comision_json.get('especialid'),
                    comision_json.get('materia'),
                    comision_json.get('comision'),
                    comision_json.get('plan')
                )
                if comision_obj:
                    docente_comisiones_qs += [comision_obj]

        comision_choices = [('', '---------')]
        for docente_comision in docente_comisiones_qs:
            comision_choices += [(
                docente_comision.id,
                docente_comision
            )]
        self.fields['comision'].widget = forms.Select(
            choices=comision_choices,
            attrs={'id': 'mat_select', 'class': 'form-control', 'disabled': 'true'})

    comision = forms.CharField(
        required=False,
        label='Comisión y Materia:',
    )

    fechaInicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'disabled': 'true'})
    )

    class Meta:
        model = Solicitud
        fields = ['fechaInicio', 'fechaFin', 'tipoSolicitud', 'comision']
        widgets = {
            'tipoSolicitud': forms.Select(attrs={'id': 'tipo_select', 'class': 'form-control', }),
            'fechaFin': forms.DateInput(attrs={'class': 'form-control', 'disabled': 'true'}),
        }

    def clean_comision(self):
        comision = self.cleaned_data['comision']
        tipo_solicitud = self.data['tipoSolicitud']
        if tipo_solicitud == '1' or tipo_solicitud == '2':
            if not comision:
                raise forms.ValidationError("La comision no puede estar vacia")
        else:
            return None
        comision_obj = Comision.objects.get(id=comision)
        return comision_obj

    def clean_fechaFin(self):
        inicio = self.cleaned_data.get('fechaInicio')
        fin = self.cleaned_data.get('fechaFin')
        tipo_solicitud = self.data.get('tipoSolicitud')
        if not fin:
            if tipo_solicitud == '1':
                comision_obj = Comision.objects.get(id=self.data.get('comision'))
                fin = obtener_fecha_fin_reserva_cursado(comision_obj.semestre)
            elif tipo_solicitud == '3':
                raise forms.ValidationError(
                    "La fecha de fin no puede ser nula"
                )
            else:
                return None
        if inicio > fin:
            raise forms.ValidationError(
                "La fecha de fin de la solicitud no puede ser menor a la fecha de inicio"
            )
        return fin

    def clean_fechaInicio(self):
        inicio = self.cleaned_data.get('fechaInicio')
        tipo_solicitud = self.data.get('tipoSolicitud')
        if not inicio:
            if tipo_solicitud == '1':
                comision_obj = Comision.objects.get(id=self.data.get('comision'))
                inicio = obtener_fecha_inicio_reserva_cursado(comision_obj.semestre)
            else:
                raise forms.ValidationError(
                    "La fecha de inicio no puede ser nula"
                )
        return inicio


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
                "La hora de fin no puede ser nula"
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
                choices=sorted(ESTADO_SOLICITUD.items()),
                widget=forms.Select(attrs={'id': 'estado_select', 'class': 'form-control'})
            )
