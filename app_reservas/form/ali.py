from django import forms
from app_reservas.models import AccesorioPrestamo, Recurso, RecursoPrestamo, Accesorio


class AliRecursoForm(forms.Form):
    recurso = forms.CharField(
        label='Recurso:',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    def clean_recurso(self):
        recurso = self.cleaned_data['recurso']
        try:
            recurso_obj = Recurso.objects.get(codigo=recurso)
        except Recurso.DoesNotExist:
            raise forms.ValidationError("El recurso ingresado no es válido. Intente nuevamente")
        if not recurso_obj.activo:
            raise forms.ValidationError("El recurso ingresado no se encuetra activo. Consulte al administrador del sistema")
        return recurso_obj


class ElementoForm(forms.Form):
    def __init__(self, request=None, *args, **kwargs):
        super(ElementoForm, self).__init__(*args, **kwargs)
        self.request = request

    recurso = forms.CharField(
        label='Recurso:',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    def clean_recurso(self):
        recurso = self.cleaned_data['recurso']
        elemento_obj = None
        try:
            elemento_obj = Recurso.objects.get(codigo=recurso)
        except Recurso.DoesNotExist:
            pass
        try:
            elemento_obj = Accesorio.objects.get(codigo=recurso)
        except Accesorio.DoesNotExist:
            pass
        recurso_list = self.request.session.get('recurso_list', [])
        accesorio_list = self.request.session.get('accesorio_list', [])
        if not elemento_obj:
            raise forms.ValidationError("El recurso ingresado no es válido. Intente nuevamente")
        if not elemento_obj.activo:
            raise forms.ValidationError("El recurso ingresado no se encuetra activo. Consulte al administrador del sistema")
        if (type(elemento_obj) is Accesorio and elemento_obj.id in accesorio_list) or \
            (type(elemento_obj) is Recurso and elemento_obj.id in recurso_list):
            raise forms.ValidationError("El recurso ingresado ya se encuentra agregado al prestamo")
        prestamo_obj = elemento_obj.get_active_loan()
        if prestamo_obj:
            raise forms.ValidationError("El recurso ingresado ya tiene un prestamo activo")
        return elemento_obj


class AccesorioPrestamoForm(forms.ModelForm):

    class Meta:
        model = AccesorioPrestamo
        fields = ['accesorio']


class RecursoPrestamoForm(forms.ModelForm):

    class Meta:
        model = RecursoPrestamo
        fields = ['recurso', 'reserva']


class PrestamoReservaForm(forms.Form):
    def __init__(self, request=None, recurso=None, *args, **kwargs):
        super(PrestamoReservaForm, self).__init__(*args, **kwargs)
        if recurso is not None and request.method == 'GET':
            self.fields['reserva'].choices = [(reserva.id, reserva) for reserva in recurso.get_nearby_reservations()] + [('', 'Crear nueva reserva')]

    reserva = forms.ChoiceField(
                choices=[(recurso.id, recurso) for recurso in Recurso.objects.all()],
                required=True,
                label='Recurso',
                widget=forms.Select(attrs={'class': 'form-control'})
            )

    def clean_recurso(self):
        cleaned_data = super(PrestamoReservaForm, self).clean()
        reserva = cleaned_data.get("reserva")
        if reserva is None:
            raise forms.ValidationError(
                "Es necesario asignar una reserva"
            )
        return reserva
