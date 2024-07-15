from django.shortcuts import render, redirect, get_object_or_404
from .forms import CrearActividad, MiFormulario, SeleccionarMateria
from .models import Actividades, Profesores, Materia, Estudiantes, Planificacion
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import random


# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')

def registrarse(request):
    if request.method == 'GET':
        return render(request,'registrarse.html',{
        'form': UserCreationForm,
        'materia': SeleccionarMateria()
    })
    else:
        user = User.objects.create_user(username=request.POST['nombre_usuario'], password = request.POST['clave1'], first_name = request.POST['nombre'], last_name = request.POST['apellido'] )
        es_estudiante = request.POST.get('es_estudiante')
        user_instancia = get_object_or_404(User, id=user.id)
        
        if es_estudiante == 'True':
            estudiante = Estudiantes(user = user_instancia, nombre = request.POST['nombre'])
            estudiante.save()
            redirect_url = '/'
        else:
            profesor = Profesores(user=user_instancia, nombre=request.POST['nombre'])
            form = SeleccionarMateria(request.POST)
            if form.is_valid():
                profesor.materia = form.cleaned_data['materia']
                profesor.save()
                redirect_url = '/'
        
        
        if request.POST['clave1'] != request.POST['clave2']:
            return render(request,'registrarse.html',{
            'form': UserCreationForm,
            'error': 'Las contraseñas no coinciden'
            })
        else:
            user.save()
            login(request, user)
            return redirect(redirect_url)

def iniciar_sesion(request):
    if request.method == 'GET':
        return render(request, 'iniciar_sesion.html',{
            'form': AuthenticationForm,
            
        })
    else:
        user = authenticate(request, username = request.POST['nombre_usuario'], password = request.POST['clave1'])
        
        if user is None:
            return render(request, 'iniciar_sesion.html',{
                'form': AuthenticationForm,
                'error': 'Usario o contraseña incorrectas'
            })
        else:
           login(request, user)
           return redirect('inicio')
        
@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')

@login_required
def crear_actividad(request):
    if request.method == 'GET':
        return render(request, 'registrar_actividad.html',{
            'form': CrearActividad(),
            'mostrar': SeleccionarMateria
        })
    else:
        form = CrearActividad(request.POST)
        materia = Materia.objects.create(nombre = request.POST['materia'])
        selectmateria = SeleccionarMateria(request.POST)
        materia.save()
        
        
        if form.is_valid() and selectmateria.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.materia = selectmateria.cleaned_data['materia']
            new_form.save()
            
            profesores = Profesores.objects.filter(materia=selectmateria.cleaned_data['materia'])
            if profesores.exists():
                random_profesor = random.choice(profesores)
                planificacion = Planificacion.objects.create(
                    actividades = new_form,
                    estudiante = request.user,
                    profesor = random_profesor
                )
                planificacion.save()

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
def calendario(request):
    if request.method == 'POST':
        form = MiFormulario(request.POST)
        if form.is_valid():
            # Process the form data
            pass
    else:
        form = MiFormulario()
    return render(request, 'calendario.html', {'form': form})

@login_required
def asignar_materia_a_profesor(request):
    if request.method == 'GET':
        datos = User.objects.get(id = request.user.id)
        return render(request, 'asignar_materia_profesor.html',{
            'datos': datos,
            'materia': SeleccionarMateria()
        })
    else:
        materia = get_object_or_404(Profesores, user = request.user.id )
        form = SeleccionarMateria(request.POST)
        if form.is_valid():
            materia.materia = form.cleaned_data['materia']
            materia.save()
            return redirect('inicio')
        
@login_required
def perfil(request, user_id):
    usuario = User.objects.get(id=user_id)
    try:
        estudiante = get_object_or_404(Estudiantes, user = user_id)
        return render(request, 'perfil.html',{
            'usuario': usuario,
            'estudiante': estudiante,
            'profesor': None
        })
    except:
        profesor = get_object_or_404(Profesores, user = user_id)
        return render(request, 'perfil.html',{
            'usuario': usuario,
            'profesor': profesor,
            'estudiante': None
        })

def planificacion(request):
    if request.method == 'GET':
        actividad = Actividades.objects.all()
        return render (request, 'planificacion.html',{
            'actvidad': actividad
        })