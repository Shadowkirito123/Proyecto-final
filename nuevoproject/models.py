from django.db import models

# Create your models here.
class Actividades(models.Model):
    materia = models.CharField(max_length=200)
    actividad = models.TextField()
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_final = models.DateTimeField(null=True, blank=True)
    importante = models.BooleanField(default=False)
    
    def __str__(self):
        return self.materia
    
class Profesores(models.Model):
    nombre = models.CharField(max_length=250)
    apellido = models.CharField(max_length=250)
    materia = models.CharField(max_length=250)
    estado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre + self.apellido