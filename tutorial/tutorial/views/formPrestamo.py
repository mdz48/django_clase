from django import forms
from ..models import Prestamo

class FormPrestamo(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = '__all__'