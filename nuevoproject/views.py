from django.shortcuts import render, redirect
from .forms import CrearActividad, CrearProfesores
from .models import Actividades, Profesores
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')

def registrarse(request):
    if request.method == 'GET':
        return render(request,'registrarse.html',{
        'form': UserCreationForm
    })
    else:
        user = User.objects.create_user(username=request.POST['nombre_usuario'], password = request.POST['clave1'] )
        if request.POST['clave1'] != request.POST['clave2']:
            return render(request,'registrarse.html',{
            'form': UserCreationForm,
            'error': 'Las contraseñas no coinciden'
            })
        else:
            user.save()
            login(request, user)
            return redirect('/')

@login_required
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

@login_required        
def mostrar_actividades(request):
    if request.method == 'GET':
        actividad = Actividades.objects.all()
        return render (request, 'actividades.html',{
            'actvidad': actividad
        })

@login_required
def filtrar_actividades_importantes(request):
    if request.method == 'POST':
        actividad = Actividades.objects.filter(importante=True)
        return render(request, 'detalles_actividades.html', {
            'actividad': actividad
        })
    else:
        pass

@login_required
def filtrar_actividades_noimportantes(request):
    if request.method == 'POST':
        actividad = Actividades.objects.filter(importante=False)
        return render(request, 'detalles_actividades.html', {
            'actividad': actividad
        })
    else:
        pass

@login_required
def profesores(request):
    if request.method == 'GET':
        profesores = Profesores.objects.all()
        return render(request, 'profesores.html',{
            'profesores': profesores
        })
    else:
        pass

@login_required
def crear_profesores(request):
    if request.method == 'GET':
        return render(request, 'crear_profesores.html', {
            'crear': CrearProfesores
        })
    else:
        form = CrearProfesores(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.save()
            return redirect('profesores')