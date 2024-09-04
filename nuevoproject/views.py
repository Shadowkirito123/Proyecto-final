from django.shortcuts import render, redirect, get_object_or_404
from .forms import CrearActividad, MiFormulario, SeleccionarMateria, SeleccionarCarrera, SeleccionarMateriasPorCarreras1, MiFormulario11, MateriaForm, CarreraFormCrear, MateriaPorCarreraCrear, MensajeForm, Actividad_lista
from .models import Actividades, Profesores, Materia, Estudiantes, Planificacion, Estdiantes_por_carreras, Materias_por_carreras, Carreras, Mensaje
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import random
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Count
from django.db.models import Q
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import re

#Para enviar token de cambio de clave
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm


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

        # validaciones
        
        # Validación del nombre de usuario
        if not re.match(r'^[a-zA-Z ]+$', request.POST['nombre_usuario']):
            return render(request,'registrarse.html',{
                'mostrar': SeleccionarMateria(),
                'carrera': SeleccionarCarrera(),
                'error': 'El nombre de usuario no es valido, no puede llevar caracteres especiales'
            })
        
        # Validación del nombre
        if not re.match(r'^[a-zA-Z ]+$', request.POST['nombre']):
            return render(request,'registrarse.html',{
                'mostrar': SeleccionarMateria(),
                'carrera': SeleccionarCarrera(),
                'error': 'El nombre no es valido, no puede llevar caracteres especiales'
            })
        
        # Validación del apellido
        if not re.match(r'^[a-zA-Z ]+$', request.POST['apellido']):
            return render(request,'registrarse.html',{
                'mostrar': SeleccionarMateria(),
                'carrera': SeleccionarCarrera(),
                'error': 'El apellido no es valido, no puede llevar caracteres especiales'
            })
        
        # Validación de cédula
        if not re.match(r'^\d{8}$', request.POST['cedula']):
            return render(request,'registrarse.html',{
                'mostrar': SeleccionarMateria(),
                'carrera': SeleccionarCarrera(),
                'error': 'La cédula no es válida'
            })

        # fin validaciones

        
        if 'no_esta' in request.POST and request.POST['no_esta'] == 'True':
            # El usuario ha seleccionado la opción de escribir una nueva materia
            materia_nueva = request.POST['materia_nueva']
            materia, created = Materia.objects.get_or_create(nombre = materia_nueva)
            
            if request.POST['clave1'] == request.POST['clave2']:
                user = User.objects.create_user(username = request.POST['nombre_usuario'], password = request.POST['clave1'], first_name = request.POST['nombre'], last_name = request.POST['apellido'], email = request.POST['correo'] )
                es_estudiante = request.POST.get('es_estudiante')
                email1 = request.POST['correo']
                user.save()
                login(request, user)
                send_mail(
                    'Hola desde django app',
                    'Felicidades has creado tu cuenta exitosamente',
                    'pruebadedjango46@gmail.com',
                    [email1],
                    fail_silently=False  
                    )
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
                    user = User.objects.create_user(username = request.POST['nombre_usuario'], password = request.POST['clave1'], first_name = request.POST['nombre'], last_name = request.POST['apellido'], email = request.POST['correo'] )
                    es_estudiante = request.POST.get('es_estudiante')
                    email1 = request.POST['correo']
                    user.save()
                    login(request, user)
                    send_mail(
                    'Hola desde django app',
                    'Felicidades has creado tu cuenta exitosamente',
                    'pruebadedjango46@gmail.com',
                    [email1],
                    fail_silently=False  
                    )
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
                if profesores.count() > 1:
                    random_profesor = random.choice(list(profesores))
                else:
                    random_profesor = profesores[0]

                planificacion = Planificacion.objects.create(
                    actividades=new_form,
                    estudiante=estudiante,
                    profesor=random_profesor
                )
                planificacion.save()
        
        else:
            if form.is_valid() and selectmateria.is_valid():
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.materia = selectmateria.cleaned_data['materia']
                new_form.save()
                
                profesores = Profesores.objects.filter(materia=selectmateria.cleaned_data['materia'])
                if profesores.count() > 1:
                    random_profesor = random.choice(list(profesores))
                else:
                    random_profesor = profesores[0]

                planificacion = Planificacion.objects.create(
                    actividades=new_form,
                    estudiante=estudiante,
                    profesor=random_profesor
                )
                planificacion.save()

        return redirect('mostrar actividades')

@login_required        
def mostrar_actividades(request):
    if request.method == 'GET':
        actividad = Actividades.objects.filter(user = request.user, completada = False)
        error = 'No hay actividades'
        return render (request, 'actividades.html',{
                'actividades': actividad,
                'error': error
            })

@login_required
def mostrar_actividades_completadas(request):
    if request.method == 'POST':
        actividad = Actividades.objects.filter(user=request.user, completada=True)
        error = 'No hay actividades completadas' if not actividad else None
        return render(request, 'actividades_completadas.html', {
            'actividades': actividad,
            'error': error
        })
        
    else:
        return HttpResponse("Método no permitido", status=405)
        
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
        cedula = Estudiantes.objects.get(user = usuario)
        return render(request, 'perfil.html',{
        'usuario': usuario,
        'cedula': cedula.cedula
        })
    except:
        cedula = Profesores.objects.get(user = usuario)
        return render(request, 'perfil.html',{
        'usuario': usuario,
        'cedula': cedula.cedula
        })
    
@login_required
def modificar_perfil(request, user_id):
    if  request.method == 'GET':
        usuario = User.objects.get(id=user_id)
        return render(request, 'perfil_modificar.html',{
            'usuario': usuario,
        })
    else:
        try:
            #Obtener datos nuevos del usuario
            dato_nombreDeusuario = request.POST['nombre_usuario']
            dato_nombreRealUsuario = request.POST['nombre_real']
            dato_correoUsuario = request.POST['correo']
            
            #Actualizar datos nuevos (Estudiante)
            datos_usuario = User.objects.get(id=user_id)
            datos_usuario2 = Estudiantes.objects.get(user = user_id)
            datos_usuario.username = dato_nombreDeusuario
            datos_usuario.first_name = dato_nombreRealUsuario
            datos_usuario2.nombre = dato_nombreRealUsuario
            datos_usuario.email = dato_correoUsuario
            datos_usuario.save()
            datos_usuario2.save()
            return redirect('perfil', user_id=user_id)
        except:
            #Actualizar datos nuevos (Profesor)
            datos_usuario = User.objects.get(id=user_id)
            datos_usuario2 = Profesores.objects.get(user = user_id)
            datos_usuario.username = dato_nombreDeusuario
            datos_usuario.first_name = dato_nombreRealUsuario
            datos_usuario2.nombre = dato_nombreRealUsuario
            datos_usuario.email = dato_correoUsuario
            datos_usuario.save()
            datos_usuario2.save()
            return redirect('perfil', user_id=user_id)

login_required
def cambio_contraseña(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Contraseña cambiada con éxito')
            return redirect('/')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'cambiar_contraseña.html', {'form': form})
        
@login_required
def planificacion(request):
    profesor_asig = get_object_or_404(Estudiantes, user = request.user)
    if request.method == 'GET':
        planificacion = Planificacion.objects.filter(estudiante = profesor_asig.pk)
        error = 'No hay nada en planificacion, tienes que crear una actividad o aún no hay profesores designados para la materia'
        return render (request, 'planificacion.html',{
            'planificacion': planificacion,
            'plani':planificacion,
            'error': error
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
        
@login_required
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
            return redirect('detalles carreras', carreras_id)
        else:
            messages.error(request, 'Error al asociar la materia a la carrera')
            return render(request, 'super_usuario_materias.html', {'asociar_materias': form})

@login_required        
def estudiante_asignado_profesor(request):
    profesor_pro = get_object_or_404(Profesores, user = request.user )
    if request.method == 'GET':
        actividad_asignada = Planificacion.objects.filter(profesor = profesor_pro)
        estudiantes_unicos = actividad_asignada.values_list('estudiante', flat=True).distinct()
        estudiantes = Estudiantes.objects.filter(id__in=estudiantes_unicos)
        return render(request, 'actividad_asignada_profesor.html', {
            'estudiantes': estudiantes
        })
 
@login_required       
def estudiante_asignado_profesor_detalle_actividad(request, estudiantes_id):
    estudiante = Estudiantes.objects.get(id = estudiantes_id)
    if request.method == 'GET':
        actividad_detalle = Planificacion.objects.filter(estudiante = estudiante, completada = False)
        cantidad_actividades = actividad_detalle.count()
        error = 'No hay actividades pendientes'
        return render(request, 'actividad_asignada_detalles.html', {
            'actividad_detalle': actividad_detalle,
            'cantidad_actividades': cantidad_actividades,
            'error': error,
            'estudiante': estudiante
        })
        
@login_required
def estudiante_asignado_profesor_detalle_verActividad(request, actividad_id):
    if request.method == 'GET':
        actividad = get_object_or_404(Planificacion, actividades = actividad_id)
        return render(request, 'actividad_asignada_profesor_verDetalles.html',{
            'actividad': actividad,
            'form': Actividad_lista()
        })
    else:
        dato_actvidad = Planificacion.objects.get(actividades = actividad_id)
        completada = 'completada' in request.POST
        dato_actvidad.completada = completada
        dato_actvidad.save()
        return redirect('detalles actividad de estudiante', estudiantes_id = dato_actvidad.estudiante.pk)

@login_required
def estudiante_asignado_profesor_detalle_actividad_completada(request, estudiante_id):
    estudiante = Estudiantes.objects.get(id = estudiante_id)
    if request.method == 'GET':
        actvidad_detalle = Planificacion.objects.filter( estudiante = estudiante, completada = True)
        cantidad_actividades = actvidad_detalle.count()
        return render(request, 'actividad_asignada_detalles_completada.html', {
            'actividad_detalle': actvidad_detalle,
            'cantidad_actividades': cantidad_actividades,
        })
    
@login_required
def enviar_mensaje(request, receptor_id):
    receptor = User.objects.get(id=receptor_id)
    emisor = request.user

    if request.method == 'POST':
        form = MensajeForm(request.POST, request.FILES, initial={'receptor': receptor})
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.emisor = emisor
            mensaje.save()
            return redirect('enviar_mensaje', receptor_id = receptor_id)
    else:
        form = MensajeForm(initial={'receptor': receptor})
        mensajes_recibidos = Mensaje.objects.filter(Q(emisor=emisor, receptor=receptor) | Q(emisor=receptor, receptor=emisor)).order_by('fecha_envio')
        return render(request, 'enviar_mensaje.html', {
            'form': form,
            'receptor': receptor,
            'mensajes_recibidos': mensajes_recibidos
        })        

@login_required
def enviar_mensaje_estudiante(request, receptor_id):
    receptor = User.objects.get(id=receptor_id)
    emisor = request.user
    if request.method == 'POST':
        form = MensajeForm(request.POST, request.FILES, initial={'receptor': receptor})
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.emisor = emisor
            mensaje.save()
            return redirect('enviar_mensaje', receptor_id = receptor_id)
    else:
        form = MensajeForm(initial={'receptor': receptor})
        mensajes_recibidos = Mensaje.objects.filter(Q(emisor=emisor, receptor=receptor) | Q(emisor=receptor, receptor=emisor)).order_by('fecha_envio')
        return render(request, 'enviar_mensaje.html', {
            'form': form,
            'receptor': receptor,
            'mensajes_recibidos': mensajes_recibidos
        })
    
@login_required
def descargar_archivo(request, pk):
    mensaje = Mensaje.objects.get(pk=pk)
    archivo = mensaje.archivo
    fs = FileSystemStorage()
    response = HttpResponse(fs.open(archivo.name, 'rb').read(), content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename="%s"' % archivo.name
    return response

@login_required
def calendario(request):
    if request.method == 'GET':
        try:
            actividades = Actividades.objects.filter(user = request.user)
            return render(request, 'calendario.html',{
                'actividades': actividades
            })
        except:
            profesor_pro = Profesores.objects.get(user=request.user)
            planificaciones = Planificacion.objects.filter(profesor=profesor_pro)
            actividades = [plan.actividades for plan in planificaciones]
            return render(request, 'calendario.html', {
                'actividades': actividades
            })

#funcion para token de la contraseña no usar
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['email']
            user = User.objects.get(email=user)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"{request.scheme}://{request.get_host()}/reset-password/{uid}/{token}/"
            subject = "Restablecer contraseña"
            message = render_to_string('password_reset_email.html', {
                'user': user,
                'reset_url': reset_url
            })
            send_mail(subject, message, 'pruebadedjango46@gmail.com', [user.email])
            return HttpResponse("Se ha enviado un correo electrónico con instrucciones para restablecer su contraseña.")
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset.html', {'form': form})

#funcion para token de la contraseña no usar
def password_reset_confirm(request, uidb64, token):
    try:
        uid = str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse("Contraseña restablecida con éxito.")
        else:
            form = SetPasswordForm(user)
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        return HttpResponse("El enlace de restablecimiento de contraseña no es válido.")