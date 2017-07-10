from django import forms
from app_reservas.models import Recurso


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
