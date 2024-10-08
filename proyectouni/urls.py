"""
URL configuration for proyectouni project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from nuevoproject import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('usuario/<int:user_id>', views.perfil, name='perfil'),
    path('usuario/modificar_perfil/<int:user_id>', views.modificar_perfil, name='modificar perfil'),
    path('usuario/cambio_contraseña/', views.cambio_contraseña, name='cambiar contraseña'),
    path('crear_actividad/', views.crear_actividad, name='actividad'),
    path('crear_actividad/otra_actividad', views.agregar_otra_actividad, name='agregar otra actividad'),
    path('mostrar_actividad/', views.mostrar_actividades, name='mostrar actividades'),
    path('mostrar_actividad/completadas', views.mostrar_actividades_completadas, name='mostrar actividades completadas'),
    path('mostrar_actividad/<int:actividad_id>/editar', views.editar_actividad, name='editar actividad'),
    path('mostrar_actividad/<int:actividad_id>/eliminar', views.eliminar_actividad, name='eliminar actividad'),
    path('mostrar_actividad/importantes', views.filtrar_actividades_importantes, name='mostrar actividades importantes'),
    path('mostrar_actividad/no_importantes', views.filtrar_actividades_noimportantes, name='mostrar actividades no importantes'),
    path('profesores/', views.profesores, name='profesores'),
    path('asignar_materia_a_profesor/', views.asignar_materia_a_profesor, name='asignar materia a profesor'),
    path('registro/', views.registrarse, name='registro'),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar sesion'),
    path('planificacion/', views.planificacion, name='planificacion'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar sesion'),
    path('calendario/', views.calendario, name='calendario_view'),
    path('agregar/', views.agregar_otra_actividad, name='agregar'),
    path("select2/", include("django_select2.urls")),
    path('sueper_usuario_usuarios/', views.super_usuario_usuarios, name='usuarios'),
    path('super_usuario_materias/', views.super_usuario_materias, name='materia'),
    path('super_usuario_materias/<int:materia_id>', views.super_usuario_elimarmateria, name='materia eliminada'),
    path('sueper_usuario_usuarios/super_usuario_usuarios_filtroprofesor/', views.super_usuario_usuarios_filtroprofesor, name='filtrar profesores'),
    path('sueper_usuario_usuarios/super_usuario_usuarios_filtroestudiante', views.super_usuario_usuarios_filtroestudiante, name='filtrar estudiante'),
    path('super_usuario_carrera/', views.super_usuario_carrera, name='super usuario carrera'),
    path('super_usuario_carrera/super_usuario_carrera_detalles/<int:carreras_id>', views.super_usuario_carrera_detalles, name='detalles carreras'),
    path('estudiante_asignado_profesor/', views.estudiante_asignado_profesor, name='estudiante asignado'),
    path('estudiante_asignado_profesor_detalle_actividad/<int:estudiantes_id>', views.estudiante_asignado_profesor_detalle_actividad, name='detalles actividad de estudiante'),
    path('estudiante_asignado_profesor_detalle_actividad/<int:actividad_id>/ver', views.estudiante_asignado_profesor_detalle_verActividad, name='ver'),
    path('estudiante_asignado_profesor/actividad_completada/<int:estudiante_id>', views.estudiante_asignado_profesor_detalle_actividad_completada, name='detalles actividad de estudiante completada'),
    path('enviar_mensaje/<int:receptor_id>/<int:actividad_id>/', views.enviar_mensaje, name='enviar_mensaje'),
    path('mensajes_estudiante/<int:receptor_id>/<int:actividad_id>', views.enviar_mensaje_estudiante, name='mensajes_estudiante'),
    path('mensajes/<pk>/descargar_archivo/', views.descargar_archivo, name='descargar_archivo'),
    #url para los tokens de la contraseña
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('reset-password/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
