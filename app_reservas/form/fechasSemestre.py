from django import forms


class FechasSemestreForm(forms.Form):

    fecha_inicio_primer_semestre = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', })
    )
    fecha_fin_primer_semestre = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', })
    )
    fecha_inicio_segundo_semestre = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', })
    )
    fecha_fin_segundo_semestre = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', })
    )
