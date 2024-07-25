from django import forms
from .models import Actividades, Materia, Carreras

class CrearActividad(forms.ModelForm):
    class Meta:
        model = Actividades
        fields = ['metas', 'tarea', 'fecha_inicio', 'fecha_final', 'importante']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_final': forms.DateInput(attrs={'type': 'date'}),
        }
        
class SeleccionarMateria(forms.ModelForm):
    materia = forms.ModelChoiceField(queryset=Materia.objects.all(), required=False)
    
    class Meta:
        model = Materia
        fields = ()
        
class SeleccionarCarrera(forms.ModelForm):
    carrera = forms.ModelChoiceField(queryset=Carreras.objects.all())
    
    class Meta:
        model = Carreras
        fields = ()

class MiFormulario(forms.Form):
    rol = forms.ChoiceField(choices=[('profesor', 'Soy profesor/docente'), ('no_profesor', 'No soy profesor/docente')])
    campo_adicional = forms.CharField(label='Campo adicional', required=False)