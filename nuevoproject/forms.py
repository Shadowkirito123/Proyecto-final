from django import forms
from .models import Actividades, Materia, Carreras, Estdiantes_por_carreras, Materias_por_carreras, Estudiantes

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
    carrera = forms.ModelChoiceField(queryset=Carreras.objects.all(), required=False)
    
    class Meta:
        model = Carreras
        fields = ()

class SeleccionarMateriasPorCarreras1(forms.ModelForm): 
    materia = forms.ModelChoiceField(queryset=Materia.objects.all())

    class Meta:
        model = Materia
        fields = ()

    def __init__(self, *args, **kwargs):
        carrera_id = kwargs.pop('carrera_id', None)
        super().__init__(*args, **kwargs)
        if carrera_id:
            materias_por_carrera = Materias_por_carreras.objects.filter(carrera_id=carrera_id)
            self.fields['materia'].queryset = Materia.objects.filter(id__in=[materia.materia_id for materia in materias_por_carrera])

class MiFormulario(forms.Form):
    rol = forms.ChoiceField(choices=[('profesor', 'Soy profesor/docente'), ('no_profesor', 'No soy profesor/docente')])
    campo_adicional = forms.CharField(label='Campo adicional', required=False)