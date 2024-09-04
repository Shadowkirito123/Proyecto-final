from django import forms
from .models import Actividades, Materia, Carreras, Materias_por_carreras, Estudiantes, Mensaje, Planificacion
from django_select2 import forms as select2_forms
import re

class CrearActividad(forms.ModelForm):
    class Meta:
        model = Actividades
        fields = ['metas', 'tarea', 'fecha_inicio', 'fecha_final', 'importante', 'completada']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_final': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        for field in ['metas', 'tarea']:
            if not re.match("^[a-zA-Z0-9\s]*$", cleaned_data.get(field, '')):
                self.add_error(field, "No se permiten caracteres especiales en este campo")
        return cleaned_data
        
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


class MiFormulario11(forms.ModelForm):
    class Meta:
        model = Estudiantes
        fields = ['user']
        
class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = ['nombre']
        
class CarreraFormCrear(forms.ModelForm):
    class Meta:
        model = Carreras
        fields = '__all__'
        
class MateriaPorCarreraCrear(forms.ModelForm):
    class Meta:
        model = Materias_por_carreras
        fields = ['materia', 'nombre']
        
    def __init__(self, *args, **kwargs):
        carrera = kwargs.pop('carrera', None)
        super(MateriaPorCarreraCrear, self).__init__(*args, **kwargs)
        if carrera:
            self.instance.carrera = carrera
            
class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ('texto', 'archivo', 'receptor')
        
class Actividad_lista(forms.ModelForm):
    class Meta:
        model = Planificacion
        fields = ['completada']