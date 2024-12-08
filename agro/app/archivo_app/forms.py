from django import forms
from .models import ArchivoEntrada

class ArchivoEntradaForm(forms.ModelForm):
    class Meta:
        model = ArchivoEntrada
        fields = ['archivo']
