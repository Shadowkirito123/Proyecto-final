from django.shortcuts import render, redirect, get_object_or_404
from .forms import CrearActividad, MiFormulario, SeleccionarMateria, SeleccionarCarrera, SeleccionarMateriasPorCarreras1
from .models import Actividades, Profesores, Materia, Estudiantes, Planificacion, Estdiantes_por_carreras
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import random
from django.template.loader import render_to_string
from django.http import HttpResponse

# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')

def registrarse(request):
    if request.method == 'GET':
        return render(request,'registrarse.html',{
            'mostrar': SeleccionarMateria(),
            'carrera': SeleccionarCarrera()
    })
    else:
        selectmateria = SeleccionarMateria(request.POST)
        selectcarrera = SeleccionarCarrera(request.POST)
        
        if 'no_esta' in request.POST and request.POST['no_esta'] == 'True':
            # El usuario ha seleccionado la opción de escribir una nueva materia
            materia_nueva = request.POST['materia_nueva']
            materia, created = Materia.objects.get_or_create(nombre = materia_nueva)
            if request.POST['clave1'] == request.POST['clave2']:
                user = User.objects.create_user(username = request.POST['nombre_usuario'], password = request.POST['clave1'], first_name = request.POST['nombre'], last_name = request.POST['apellido'] )
                es_estudiante = request.POST.get('es_estudiante')
                user.save()
                login(request, user)
                if es_estudiante == 'True':
                    estudiante = Estudiantes(user = request.user, nombre = request.POST['nombre'])
                    estudiante.save()
                    redirect_url = '/'
                else:
                    profesor = Profesores(user = request.user, nombre = request.POST['nombre'], materia = materia)
                    profesor.save()
                    redirect_url = '/'
        
        else:
            if selectmateria.is_valid() and selectcarrera.is_valid():
                if request.POST['clave1'] == request.POST['clave2']:
                    user = User.objects.create_user(username = request.POST['nombre_usuario'], password = request.POST['clave1'], first_name = request.POST['nombre'], last_name = request.POST['apellido'] )
                    es_estudiante = request.POST.get('es_estudiante')
                    user.save()
                    login(request, user)
                    if es_estudiante == 'True':
                        estudiante = Estudiantes(user = request.user, nombre = request.POST['nombre'], carrera = selectcarrera.cleaned_data['carrera'])
                        estudiante.save()
                        estudiante_por_carrera = Estdiantes_por_carreras(carrera = selectcarrera.cleaned_data['carrera'], estudiante = request.user, nombre = request.POST['nombre'])
                        estudiante_por_carrera.save()
                        redirect_url = '/'
                    else:
                        profesor = Profesores(user = request.user, nombre = request.POST['nombre'], materia = selectmateria.cleaned_data['materia'])
                        profesor.save()
                        redirect_url = '/'
                
                else:
                    return render(request,'registrarse.html',{
                        'form': UserCreationForm,
                        'materia': SeleccionarMateria(),
                        'error': 'Las contraseñas no coinciden'
                    })
                
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
    estudiante = Estudiantes.objects.get(user = request.user)
    carrera_id = estudiante.carrera
    if request.method == 'GET':
        return render(request, 'registrar_actividad.html',{
            'form': CrearActividad(),
            'mostrar': SeleccionarMateria(),
            'carrera1': SeleccionarMateriasPorCarreras1(carrera_id = carrera_id)
        })
    else:
        form = CrearActividad(request.POST)
        selectmateria = SeleccionarMateriasPorCarreras1(request.POST)  
        
        if 'no_esta' in request.POST and request.POST['no_esta'] == 'True':
            # El usuario ha seleccionado la opción de escribir una nueva materia
            materia_nueva = request.POST['materia_nueva']
            materia, created = Materia.objects.get_or_create(nombre = materia_nueva)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.materia = materia
                new_form.save()
                
                profesores = Profesores.objects.filter(materia=materia)
                if profesores.exists():
                    random_profesor = random.choice(profesores)
                    planificacion = Planificacion.objects.create(
                        actividades = new_form,
                        estudiante = request.user,
                        profesor = random_profesor
                    )
                    planificacion.save()
        
        else:
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
        actividad = Actividades.objects.filter(user = request.user)
        error = 'No hay actividades'
        return render (request, 'actividades.html',{
                'actvidad': actividad,
                'error': error
            })

@login_required
def editar_actividad(request, actividad_id):
    if request.method == 'GET':
        actividad = get_object_or_404(Actividades, pk = actividad_id, user = request.user)
        crear_actividad = CrearActividad(instance=actividad)
        return render(request, 'editar_actividad.html', {
            'actividad': actividad,
            'crear': crear_actividad
        })
    else:
        try:
            actividad = get_object_or_404(Actividades, pk = actividad_id, user = request.user)
            crear_actividad = CrearActividad(request.POST, instance=actividad)
            crear_actividad.save()
            return redirect('mostrar actividades')
        except:
            return render(request, 'editar_actividad.html', {
            'actividad': actividad,
            'crear': crear_actividad,
            'error': 'Error al actualizar'
        })

@login_required
def eliminar_actividad(request, actividad_id):
    actividad = get_object_or_404(Actividades, pk=actividad_id, user = request.user)
    if request.method == 'POST':
        actividad.delete()
        return redirect('mostrar actividades')

@login_required
def filtrar_actividades_importantes(request):
    if request.method == 'POST':
        actividad = Actividades.objects.filter(importante=True, user = request.user)
        return render(request, 'detalles_actividades.html', {
            'actividad': actividad
        })
    else:
        pass

@login_required
def filtrar_actividades_noimportantes(request):
    if request.method == 'POST':
        actividad = Actividades.objects.filter(importante=False, user = request.user)
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

@login_required
def planificacion(request):
    if request.method == 'GET':
        planificacion = Planificacion.objects.get(estudiante = request.user.id)
        return render (request, 'planificacion.html',{
            'planificacion': planificacion
        })

def agregar_otra_actividad(request):
    if request.method == 'GET':
        form = CrearActividad()
        html = render_to_string('agregar_otra_actividad.html', {'form': form})
        return HttpResponse(html, content_type = 'text/html')
    
