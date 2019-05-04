from datetime import datetime
from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet

from app_reservas.models import (
    HorarioReserva,
    Recurso,
    Reserva,
)

from app_reservas.models.solicitud import TIPO_SOLICITUD

from app_academica.models import Comision, Docente
from app_reservas.services.reservas import get_nombre_evento

from app_reservas.utils import (
    obtener_fecha_inicio_reserva_cursado,
    obtener_fecha_fin_reserva_cursado,
    obtener_horario_comision,
    obtener_recurso,
    obtener_recursos_asignables, get_now_timezone)

from app_reservas.models.historicoEstadoReserva import ESTADO_RESERVA

INVALID_SCHEDULE_MESSAGE = "La comisión no tiene horarios disponibles"
LOWER_END_HOUR_MESSAGE = "La hora de fin no puede ser menor a la hora de inicio"
INVALID_DAY_MESSAGE = "El día seleccionado no corresponde con el día de la fecha de inicio"
EMPTY_DAY_MESSAGE = "El campo día no puede estar vacío"


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
        cleaned_data = super(HorarioReservaForm, self).clean()
        recurso = cleaned_data.get("recurso")
        if recurso is None:
            # Only do something if both fields are valid so far.
            raise forms.ValidationError(
                "Es necesario asignar un recurso"
            )
        recurso_list = Recurso.objects.filter(pk=recurso)
        if not recurso_list:
            raise forms.ValidationError(
                "El recurso ingresado no es válido"
            )
        return recurso_list[0]

    def clean(self):
        super(HorarioReservaForm, self).clean()

        reserva_form = ReservaCreateForm(self.data)
        if reserva_form.is_valid():
            dia = self.cleaned_data.get('dia')
            tipo_solicitud = reserva_form.cleaned_data.get('tipo_solicitud')

            # Validación de horarios de comisión
            if tipo_solicitud == '1' or tipo_solicitud == '2':
                if str(dia) == 'None':
                    raise forms.ValidationError(
                        EMPTY_DAY_MESSAGE
                    )
                comision = reserva_form.cleaned_data.get('comision')
                horario = obtener_horario_comision(comision, int(dia))

                if not horario:
                    raise forms.ValidationError(
                        INVALID_SCHEDULE_MESSAGE
                    )
                hora_inicio_comision = datetime.strptime(horario.get('hora_inicio'), '%H:%M').time()
                hora_fin_comision = datetime.strptime(horario.get('hora_fin'), '%H:%M').time()

                if self.cleaned_data.get('inicio') < hora_inicio_comision or\
                    self.cleaned_data.get('inicio') > hora_fin_comision or \
                    self.cleaned_data.get('fin') < hora_inicio_comision or\
                    self.cleaned_data.get('fin') > hora_fin_comision:
                        raise forms.ValidationError(
                            INVALID_SCHEDULE_MESSAGE
                        )

            fecha_inicio = reserva_form.cleaned_data.get('fecha_inicio')
            if tipo_solicitud == '2' or tipo_solicitud == '4':
                if fecha_inicio.weekday() != int(dia):
                    raise forms.ValidationError(
                        INVALID_DAY_MESSAGE
                    )

            # Validación de disponibilidad de recurso

            fecha_fin = reserva_form.cleaned_data.get('fecha_fin')

            recurso = self.cleaned_data.get('recurso')

            # reservas_qs = buscar_reservas_activas_por_fechas(recurso, fecha_inicio, fecha_fin, dia)
            #
            # if reservas_qs:
            #     from app_reservas.views.prestamo import PRESTAMO_CON_RESERVA_MESSAGE
            #
            #     raise forms.ValidationError(
            #         PRESTAMO_CON_RESERVA_MESSAGE
            #     )


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

    nombre_evento = forms.CharField(
        label='Nombre del Evento:',
        widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': 'true'}),
        required=False,
    )

    class Meta:
        model = Reserva
        fields = ['fecha_inicio', 'fecha_fin', 'docente', 'tipo_solicitud', 'comision']
        widgets = {
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'disabled': 'true'}),
        }

    def clean_comision(self):
        comision = self.cleaned_data['comision']
        tipo_solicitud = self.data.get('tipo_solicitud')
        if not tipo_solicitud:
            raise forms.ValidationError(
                "El tipo de solicitud no puede ser nulo"
            )
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
                LOWER_END_HOUR_MESSAGE
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


    def clean_nombre_evento(self):
        nombre_evento = self.cleaned_data.get('nombre_evento')
        tipo_solicitud = self.data.get('tipo_solicitud')
        comision_obj = None
        try:
            usuario_obj = Docente.objects.get(legajo=self.data.get('docente'))
        except:
            raise forms.ValidationError(
                "El docente ingresado no es válido"
            )

        if not nombre_evento or nombre_evento == '':
            if tipo_solicitud == '1' or tipo_solicitud == '2':
                try:
                    comision_obj = Comision.objects.get(id=self.data.get('comision'))
                except Comision.DoesNotExist:
                    raise forms.ValidationError(
                        "La comisión ingresada no es válida"
                    )

            else:
                raise forms.ValidationError(
                    "El nombre del evento no puede ser nulo"
                )

        cleaned_nombre_evento = get_nombre_evento(usuario_obj, comision_obj, nombre_evento)
        return cleaned_nombre_evento


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
                try:
                    comision_obj = Comision.objects.get(id=self.data.get('comision'))
                except Comision.DoesNotExist:
                    raise forms.ValidationError(
                        "La comisión ingresada no es válida"
                    )
                try:
                    usuario_obj = Docente.objects.get(legajo=self.data.get('docente'))
                except:
                    raise forms.ValidationError(
                        "El docente ingresado no es válido"
                    )

                nombre_evento = "{0!s} - {1!s} - {2!s}".format(comision_obj.materia.nombre, comision_obj.comision, usuario_obj.nombre)
            else:
                raise forms.ValidationError(
                    "El nombre del evento no puede ser nulo"
                )
        return nombre_evento

    def clean_fin(self):
        from datetime import datetime
        tipo_solicitud = self.data.get('tipo_solicitud')
        if tipo_solicitud == '2':
            comision_obj = Comision.objects.get(id=self.data['comision'])
            horario = obtener_horario_comision(comision_obj)

            fin = None
            if horario:
                fin = datetime.strptime(horario['hora_fin'], "%H:%M").time()

            if not horario or (horario and fin < get_now_timezone().time()):
                raise forms.ValidationError(
                    INVALID_SCHEDULE_MESSAGE
                )

        elif tipo_solicitud == '4':
            fin = self.cleaned_data['fin']
            if fin < get_now_timezone().time():
                raise forms.ValidationError(
                    LOWER_END_HOUR_MESSAGE
                )
        else:
            raise forms.ValidationError(
                "La fecha de fin no puede ser nula"
            )
        return fin
