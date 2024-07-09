from django import forms
from .models import Actividades

class CrearActividad(forms.ModelForm):
    class Meta:
        model = Actividades
        fields = ['materia', 'actividad', 'fecha_inicio', 'fecha_final', 'importante']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_final': forms.DateInput(attrs={'type': 'date'}),
        }