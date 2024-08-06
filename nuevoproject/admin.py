from django.contrib import admin
from .models import Actividades, Materia, Carreras, Materias_por_carreras, Profesores
# Register your models here.
admin.site.register(Actividades)
admin.site.register(Materia)
admin.site.register(Carreras)
admin.site.register(Materias_por_carreras)
admin.site.register(Profesores)