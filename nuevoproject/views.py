from django.shortcuts import render, redirect, get_object_or_404
from .forms import CrearActividad, MiFormulario, SeleccionarMateria, SeleccionarCarrera, SeleccionarMateriasPorCarreras1, MiFormulario11, MateriaForm, CarreraFormCrear, MateriaPorCarreraCrear
from .models import Actividades, Profesores, Materia, Estudiantes, Planificacion, Estdiantes_por_carreras, Materias_por_carreras, Carreras
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import random
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Count

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
                    estudiante = Estudiantes(user = request.user, nombre = request.POST['nombre'], cedula = request.POST['cedula'])
                    estudiante.save()
                    redirect_url = '/'
                else:
                    profesor = Profesores(user = request.user, nombre = request.POST['nombre'], materia = materia, cedula = request.POST['cedula'], es_profesor = True)
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
                        estudiante = Estudiantes(user = request.user, nombre = request.POST['nombre'], carrera = selectcarrera.cleaned_data['carrera'], cedula = request.POST['cedula'])
                        estudiante.save()
                        estudiante_por_carrera = Estdiantes_por_carreras(carrera = selectcarrera.cleaned_data['carrera'], estudiante = request.user, nombre = request.POST['nombre'])
                        estudiante_por_carrera.save()
                        redirect_url = '/'
                    else:
                        profesor = Profesores(user = request.user, nombre = request.POST['nombre'], materia = selectmateria.cleaned_data['materia'], cedula = request.POST['cedula'], es_profesor = True)
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
            'carrera1': SeleccionarMateriasPorCarreras1(carrera_id = carrera_id),
            'hola':MiFormulario11()
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
    return render(request, 'perfil.html',{
        'usuario': usuario
        })

@login_required
def planificacion(request):
    if request.method == 'GET':
        planificacion = Planificacion.objects.filter(estudiante = request.user.id)
        return render (request, 'planificacion.html',{
            'planificacion': planificacion
        })

def agregar_otra_actividad(request):
    if request.method == 'GET':
        form = CrearActividad()
        html = render_to_string('agregar_otra_actividad.html', {'form': form})
        return HttpResponse(html, content_type = 'text/html')

@login_required
def super_usuario_usuarios(request):
    if request.method == 'GET':
        return render(request, 'super_user_usuarios.html', {
            'form': User.objects.all()
        })

@login_required
def super_usuario_usuarios_filtroprofesor(request):
    if request.method == 'POST':
        usuario = Profesores.objects.all()
        return render(request, 'super_usuario_usuarios_filtrado.html',{
                    'form':usuario
        })

@login_required
def super_usuario_usuarios_filtroestudiante(request):
    if request.method == 'POST':
        usuario = Estudiantes.objects.all()
        return render(request, 'super_usuario_usuarios_filtrado.html',{
                    'form':usuario
        })

@login_required        
def super_usuario_materias(request):
    if request.method == 'GET':
        materias = Materia.objects.all()
        return render(request, 'super_usuario_materias.html', {'materias': materias, 'form':MateriaForm()})
    else:
        form = MateriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Materia creada con éxito')
            return redirect('materia')
        else:
            messages.error(request, 'Error al crear materia')
            return render(request, 'super_usuario_materias.html', {'form': form})

@login_required
def super_usuario_elimarmateria(request,materia_id):
    materia = get_object_or_404(Materia, pk=materia_id)
    if request.method == 'POST':
        materia.delete()
        return redirect('materia')
    
@login_required
def super_usuario_carrera(request):
    if request.method == 'GET':
        carrera = Carreras.objects.annotate(num_estudiantes=Count('estudiantes'))

        return render(request, 'super_usuario_carrera.html',{
            'carrera': carrera,
            'crear_carrera': CarreraFormCrear()
        })
    else:
        form = CarreraFormCrear(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Carrera creada con éxito')
            return redirect('super usuario carrera')
        else:
            messages.error(request, 'Error al crear la carrera')
            return render(request, 'super_usuario_materias.html', {'crear_carrera': form})
        
def super_usuario_carrera_detalles(request,carreras_id):
    carrera = get_object_or_404(Carreras, pk=carreras_id)
    if request.method == 'GET':
        carreras = Materias_por_carreras.objects.filter(carrera = carreras_id)
        form = MateriaPorCarreraCrear(carrera=carrera)
        return render(request, 'super_usuario_carrera_detalles.html',{
            'carreras': carreras,
            'asociar_materias': form
        })
    else:
        form = MateriaPorCarreraCrear(request.POST, carrera=carrera)
        if form.is_valid():
            form.save()
            messages.success(request, 'Materia asociada a carrera con éxito')
            return redirect('super usuario carrera')
        else:
            messages.error(request, 'Error al asociar la materia a la carrera')
            return render(request, 'super_usuario_materias.html', {'asociar_materias': form})