from django import forms
from ..models import Autor

class FormAutor(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nombre', 'apellido', 'fecha_nacimiento']