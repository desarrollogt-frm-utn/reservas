from django import forms
from app_usuarios.models import Docente
from app_usuarios.utils import validateEmail
from captcha.fields import CaptchaField
from django.utils.translation import ugettext as _


EMAIL_EXTENSION = (
    ("1", '@frm.utn.edu.ar'),
    ('2', '@docentes.frm.utn.edu.ar'),
    ('3', '@tic.frm.utn.edu.ar'),
)


ESTADO_USUARIO = {
    '0': _(u'Todos'),
    '1': _(u'Activo'),
    '2': _(u'Inactivo'),
}

class CreateDocenteForm(forms.Form):
    email_extesion = forms.ChoiceField(
        choices=EMAIL_EXTENSION,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    captcha = CaptchaField(label="Código de verificación")

    def clean_email(self):
        email = self.cleaned_data['email']
        email_extesion = self.cleaned_data['email_extesion']
        email_extesions = dict(EMAIL_EXTENSION)
        complete_email = email + email_extesions[email_extesion]
        if validateEmail(complete_email):
            return complete_email
        raise forms.ValidationError(
            "{0!s} no es un mail válido".format(complete_email)
        )

class CreateDocenteConfirmForm(forms.ModelForm):
    password = forms.TextInput(attrs={'class': 'form-control'})
    password_confirm = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Docente
        fields = ['password', 'first_name', 'last_name', 'foto', 'legajo', 'celular', 'telefono']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'legajo': forms.NumberInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super(CreateDocenteConfirmForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.pop("password_confirm")

        if password != confirm_password:
            raise forms.ValidationError(
                "Las contraseñas ingresadas no coinciden"
            )

class FilterUsuariosForm(forms.Form):
    estado = forms.ChoiceField(
                choices=sorted(ESTADO_USUARIO.items()),
                widget=forms.Select(attrs={'id': 'estado_select', 'class': 'form-control'})
            )
