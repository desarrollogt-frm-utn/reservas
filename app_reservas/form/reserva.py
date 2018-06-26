from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone

from app_reservas.models import (
    HorarioSolicitud,
    Recurso,
    Solicitud,
)

from app_usuarios.models import Usuario

from app_academica.models import Comision

from app_reservas.utils import (
    obtener_fecha_inicio_reserva_cursado,
    obtener_fecha_fin_reserva_cursado,
    obtener_modelo_recurso,
)

from app_reservas.models.historicoEstadoReserva import ESTADO_RESERVA

class ReservaAssignForm(forms.Form):
    def __init__(self, request=None, model=None, *args, **kwargs):
        super(ReservaAssignForm, self).__init__(*args, **kwargs)
        if model is not None and request.method == 'GET':
            self.fields['recurso'].choices = [(recurso.id, recurso) for recurso in model.objects.all()]

    recurso = forms.ChoiceField(
                choices=[(recurso.id, recurso) for recurso in Recurso.objects.all()],
                required=True,
                label='Recurso',
                widget=forms.Select(attrs={'class': 'form-control'})
            )

    def clean_recurso(self):
        cleaned_data = super(ReservaAssignForm, self).clean()
        recurso = cleaned_data.get("recurso")
        if recurso is None:
            # Only do something if both fields are valid so far.
            raise forms.ValidationError(
                "Es necesario asignar un recurso"
            )
        return recurso


class HorarioReservaForm(forms.ModelForm):

    recurso = forms.ChoiceField(
                choices=[(recurso.id, recurso) for recurso in Recurso.objects.all()],
                required=True,
                label='Recurso',
                widget=forms.Select(attrs={'class': 'form-control'})
            )

    def clean_recurso(self):
        cleaned_data = super(HorarioReservaForm, self).clean()
        recurso = cleaned_data.get("recurso")
        if recurso is None:
            # Only do something if both fields are valid so far.
            raise forms.ValidationError(
                "Es necesario asignar un recurso"
            )
        return recurso

    class Meta:
        model = HorarioSolicitud
        fields = ['dia', 'inicio', 'fin', 'cantidad_alumnos', 'recurso']
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


class ReservaCreateForm(forms.ModelForm):

    def __init__(self, request=None, changeOptions=False, *args, **kwargs):
        super(ReservaCreateForm, self).__init__(*args, **kwargs)
        if changeOptions and request.method == 'GET':
            self.fields['tipoSolicitud'].choices = [('', '---------'),('2','Cursado'),('4','Fuera de Horario')]

    comision = forms.CharField(
        required=False,
        label='Comisión y Materia:',
        widget=forms.Select(attrs={'id': 'mat_select', 'class': 'form-control', 'disabled': 'true'}),
    )

    fechaInicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'disabled': 'true'})
    )

    class Meta:
        model = Solicitud
        fields = ['fechaInicio', 'fechaFin', 'docente', 'tipoSolicitud', 'comision']
        widgets = {
            'docente': forms.Select(attrs={'id': 'docente_select', 'class': 'form-control'}),
            'tipoSolicitud': forms.Select(attrs={'id': 'tipo_select', 'class': 'form-control', 'disabled': 'true'}),
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
        tipo_solicitud = self.cleaned_data.get('tipoSolicitud')
        if not fin:
            if tipo_solicitud == '1':
                comision_obj = Comision.objects.get(id=self.cleaned_data['comision'])
                fin = obtener_fecha_fin_reserva_cursado(comision_obj.cuatrimestre)
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
                inicio = obtener_fecha_inicio_reserva_cursado(comision_obj.cuatrimestre)
            else:
                raise forms.ValidationError(
                    "La fecha de inicio no puede ser nula"
                )
        return inicio


ReservaInlineFormset = inlineformset_factory(Solicitud, HorarioSolicitud, form=HorarioReservaForm, extra=3)


class FilterReservaForm(forms.Form):
    estado = forms.ChoiceField(
                choices=sorted(ESTADO_RESERVA.items()),
                widget=forms.Select(attrs={'id': 'estado_select', 'class': 'form-control'})
            )


class ReservaWithoutSolicitudCreateForm(forms.Form):

    comision = forms.CharField(
        required=False,
        label='Comisión y Materia:',
        widget=forms.Select(attrs={'id': 'mat_select', 'class': 'form-control', 'disabled': 'true'}),
    )

    fechaInicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'disabled': 'true'})
    )
    tipoSolicitud = forms.ChoiceField(
        label='Comisión y Materia:',
        choices=[('', '---------'),('2','Cursado'),('4','Fuera de Horario')],
        widget=forms.Select(
            attrs={'id': 'tipo_select', 'class': 'form-control', 'disabled': 'true'}),
    )
    docente = forms.ChoiceField(
        label='Usuario:',
        choices=[('', '---------')] + [(user.id, user) for user in Usuario.objects.all()],
        widget=forms.Select(attrs={'id': 'docente_select', 'class': 'form-control'}),
    )
    nombreEvento = forms.CharField(
        label='Nombre del Evento:',
        widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'true'}),
        required=False,
    )

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

    def clean_docente(self):
        usuario = self.data['usuario']
        usuario_obj = Usuario.objects.get(id=usuario)
        return usuario_obj

    def clean_fechaFin(self):
        inicio = self.cleaned_data.get('fechaInicio')
        fin = self.cleaned_data.get('fechaFin')
        tipo_solicitud = self.cleaned_data.get('tipoSolicitud')
        if not fin:
            if tipo_solicitud == '1':
                comision_obj = Comision.objects.get(id=self.cleaned_data['comision'])
                fin = obtener_fecha_fin_reserva_cursado(comision_obj.cuatrimestre)
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
                inicio = obtener_fecha_inicio_reserva_cursado(comision_obj.cuatrimestre)
            elif tipo_solicitud == '2' or tipo_solicitud == '4':
                inicio = timezone.localtime(timezone.now()).date()
            else:
                raise forms.ValidationError(
                    "La fecha de inicio no puede ser nula"
                )
        return inicio

    def clean_nombreEvento(self):
        nombre_evento = self.cleaned_data.get('nombreEvento')
        tipo_solicitud = self.data.get('tipoSolicitud')
        if not nombre_evento or nombre_evento == '':
            if tipo_solicitud == '1' or tipo_solicitud == '2':
                comision_obj = Comision.objects.get(id=self.data.get('comision'))
                usuario_obj = Usuario.objects.get(id=self.data.get('docente'))
                nombre_evento = "{0!s} - {1!s} - {2!s}".format(comision_obj.materia.nombre, comision_obj.comision, usuario_obj.nombre)
            else:
                raise forms.ValidationError(
                    "El nombre del evento no puede ser nulo"
                )
        return nombre_evento
