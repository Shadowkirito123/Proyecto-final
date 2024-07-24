from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Materia(models.Model):
    nombre = models.CharField(max_length=250)
    
    def __str__(self):
        return self.nombre

class Actividades(models.Model):
    metas = models.TextField()
    tarea = models.TextField(null=True)
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_final = models.DateTimeField(null=True, blank=True)
    importante = models.BooleanField(default=False)
    materia = models.ForeignKey(Materia, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=None)

    def __str__(self):
        return self.metas

class Profesores(models.Model):
    nombre = models.CharField(max_length=250, default=None)
    materia = models.ForeignKey(Materia, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profesor', default=None)

    def __str__(self):
        return self.nombre
    
class Estudiantes(models.Model):
    nombre = models.CharField(max_length=250, default=None)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    
class Profesores_asignados_Estudiantes(models.Model):
    profesor = models.ForeignKey(Profesores, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiantes, on_delete=models.CASCADE)
    
class Planificacion(models.Model):
    actividades = models.ForeignKey(Actividades, on_delete=models.CASCADE)
    profesor = models.ForeignKey(Profesores, on_delete=models.CASCADE, default=None)
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

class Carreras(models.Model):
    nombre = models.CharField(max_length=250, default=None)
    
class Materias_por_Carreras(models.Model):
    nombre = models.CharField(max_length=250, default=None)
    carrera = models.ForeignKey(Carreras, on_delete=models.CASCADE, default=None)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, default=None)