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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    
class Estudiantes(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=None)