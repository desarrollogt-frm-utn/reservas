from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet

from app_reservas.models import (
    HorarioReserva,
    Recurso,
    Reserva,
)

from app_reservas.models.solicitud import TIPO_SOLICITUD

from app_usuarios.models import Usuario

from app_academica.models import Comision, Docente

from app_reservas.utils import (
    obtener_fecha_inicio_reserva_cursado,
    obtener_fecha_fin_reserva_cursado,
    obtener_recurso,
    obtener_recursos_asignables)

from app_reservas.models.historicoEstadoReserva import ESTADO_RESERVA

class ReservaAssignForm(forms.Form):
    def __init__(self, request=None, model=None, *args, **kwargs):
        super(ReservaAssignForm, self).__init__(*args, **kwargs)
        if model is not None and request.method == 'GET':
            self.fields['recurso'].choices = [(recurso.id, obtener_recurso(recurso.id)) for recurso in model.objects.all()]

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
                choices=[(recurso.id, obtener_recurso(recurso.id)) for recurso in Recurso.objects.all()],
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
        model = HorarioReserva
        fields = ['dia', 'inicio', 'fin', 'recurso']
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

    def clean_recurso(self):
        reserva_id = self.cleaned_data.get('recurso')
        recurso_list = Recurso.objects.filter(pk=reserva_id)
        if not recurso_list:
            raise forms.ValidationError(
                "El recurso ingresado no es válido"
            )
        return recurso_list[0]


class ReservaCreateForm(forms.ModelForm):

    def __init__(self, request=None, changeOptions=False, *args, **kwargs):
        super(ReservaCreateForm, self).__init__(request, *args, **kwargs)
        if changeOptions and request.method == 'GET':
            self.fields['tipo_solicitud'].choices = [('', '---------'),('2','Cursado'),('4','Fuera de Agenda')]

    comision = forms.CharField(
        required=False,
        label='Comisión y Materia:',
        widget=forms.Select(attrs={'id': 'mat_select', 'class': 'form-control', 'disabled': 'true'}),
    )

    fecha_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'disabled': 'true'})
    )

    docente = forms.ModelChoiceField(
        queryset=Docente.objects.all(),
        to_field_name='legajo',
        widget=forms.Select(attrs={'id': 'docente_select', 'class': 'form-control'}),
    )

    tipo_solicitud = forms.ChoiceField(
        choices=[('','---------')] +list(sorted(TIPO_SOLICITUD.items())),
        widget=forms.Select(attrs={'id': 'tipo_select', 'class': 'form-control', 'disabled': 'true'}),
    )

    class Meta:
        model = Reserva
        fields = ['fecha_inicio', 'fecha_fin', 'docente', 'tipo_solicitud', 'comision']
        widgets = {
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'disabled': 'true'}),
        }

    def clean_comision(self):
        comision = self.cleaned_data['comision']
        tipo_solicitud = self.data['tipo_solicitud']
        if tipo_solicitud == '1' or tipo_solicitud == '2':
            if not comision:
                raise forms.ValidationError("La comision no puede estar vacia")
        else:
            return None
        comision_obj = Comision.objects.get(id=comision)
        return comision_obj

    def clean_fecha_fin(self):
        inicio = self.cleaned_data.get('fecha_inicio')
        fin = self.cleaned_data.get('fecha_fin')
        tipo_solicitud = self.data.get('tipo_solicitud')
        if not fin:
            if tipo_solicitud == '1':
                comision_obj = Comision.objects.get(id=self.data['comision'])
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

    def clean_fecha_inicio(self):
        inicio = self.cleaned_data.get('fecha_inicio')
        tipo_solicitud = self.data.get('tipo_solicitud')
        if not inicio:
            if tipo_solicitud == '1':
                comision_obj = Comision.objects.get(id=self.data.get('comision'))
                inicio = obtener_fecha_inicio_reserva_cursado(comision_obj.semestre)
            else:
                raise forms.ValidationError(
                    "La fecha de inicio no puede ser nula"
                )
        return inicio


class BaseFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        request = None
        if 'request' in kwargs:
            request = kwargs.pop("request")
        super(BaseFormSet, self).__init__(*args, **kwargs)
        if request:
            for form in self.forms:
                choices = [(recurso.id, obtener_recurso(recurso.id)) for recurso in obtener_recursos_asignables(request.user)]
                if not choices:
                    choices = [('','--------')]
                form.fields['recurso'].choices = choices



ReservaInlineFormset = inlineformset_factory(Reserva, HorarioReserva, form=HorarioReservaForm, formset=BaseFormSet, extra=3)


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

    fin = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'class': 'form-control', 'disabled': 'true'})
    )
    tipo_solicitud = forms.ChoiceField(
        label='Comisión y Materia:',
        choices=[('', '---------'),('2','Cursado'),('4','Fuera de Horario')],
        widget=forms.Select(
            attrs={'id': 'tipo_select', 'class': 'form-control', 'disabled': 'true'}),
    )
    docente = forms.ModelChoiceField(
        queryset=Docente.objects.all(),
        to_field_name='legajo',
        widget=forms.Select(attrs={'id': 'docente_select', 'class': 'form-control'}),
    )
    nombre_evento = forms.CharField(
        label='Nombre del Evento:',
        widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'true'}),
        required=False,
    )

    def clean_comision(self):
        comision = self.cleaned_data['comision']
        tipo_solicitud = self.data['tipo_solicitud']
        if tipo_solicitud == '1' or tipo_solicitud == '2':
            if not comision:
                raise forms.ValidationError("La comision no puede estar vacia")
        else:
            return None
        comision_obj = Comision.objects.get(id=comision)
        return comision_obj

    def clean_docente(self):
        legajo = self.data['docente']
        docente_list = Docente.objects.filter(legajo=legajo)
        if not docente_list:
            raise forms.ValidationError("Docente no valido")
        return docente_list[0]

    def clean_nombre_evento(self):
        nombre_evento = self.cleaned_data.get('nombre_evento')
        tipo_solicitud = self.data.get('tipo_solicitud')
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

    def clean_fin(self):
        fin = self.cleaned_data['fin']
        if not fin:
            raise forms.ValidationError(
                "La hora de fin no puede ser nula"
            )
        import datetime
        if fin < datetime.datetime.now().time():
            raise forms.ValidationError(
                "La hora de fin de la solicitud no puede ser menor a la hora de inicio"
            )
        return fin
