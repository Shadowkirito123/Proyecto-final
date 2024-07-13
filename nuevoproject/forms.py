from django import forms
from .models import Actividades, Profesores, Materia
class CrearActividad(forms.ModelForm):
    class Meta:
        model = Actividades
        fields = ['metas', 'tarea', 'fecha_inicio', 'fecha_final', 'importante']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_final': forms.DateInput(attrs={'type': 'date'}),
        }

class CrearProfesores(forms.ModelForm):
    class Meta:
        model = Profesores
        fields = '__all__'
        
class SeleccionarMateria(forms.ModelForm):
    materia = forms.ModelChoiceField(queryset=Materia.objects.all())
    
    class Meta:
        model = Materia
        fields = ()