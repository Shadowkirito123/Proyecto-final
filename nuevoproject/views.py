from django.shortcuts import render, redirect
from .forms import CrearActividad, CrearProfesores
from .models import Actividades, Profesores

# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')

def crear_actividad(request):
    if request.method == 'GET':
        return render(request, 'registrar_actividad.html',{
            'form': CrearActividad()
        })
    else:
        form = CrearActividad(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.save()
            return redirect('mostrar actividades')
        
def mostrar_actividades(request):
    if request.method == 'GET':
        actividad = Actividades.objects.all()
        return render (request, 'actividades.html',{
            'actvidad': actividad
        })
        
def filtrar_actividades_importantes(request):
    if request.method == 'POST':
        actividad = Actividades.objects.filter(importante=True)
        return render(request, 'detalles_actividades.html', {
            'actividad': actividad
        })
    else:
        pass

def filtrar_actividades_noimportantes(request):
    if request.method == 'POST':
        actividad = Actividades.objects.filter(importante=False)
        return render(request, 'detalles_actividades.html', {
            'actividad': actividad
        })
    else:
        pass

def profesores(request):
    if request.method == 'GET':
        profesores = Profesores.objects.all()
        return render(request, 'profesores.html',{
            'profesores': profesores
        })
    else:
        pass
    
def crear_profesores(request):
    return render(request, 'crear_profesores.html')