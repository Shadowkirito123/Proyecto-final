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
from django.urls import path
from nuevoproject import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('usuario/<int:user_id>', views.perfil, name='perfil'),
    path('crear_actividad/', views.crear_actividad, name='actividad'),
    path('mostrar_actividad/', views.mostrar_actividades, name='mostrar actividades'),
    path('mostrar_actividad/editar', views.editar_actividad, name='editar actividad'),
    path('mostrar_actividad/eliminar', views.eliminar_actividad, name='eliminar actividad'),
    path('mostrar_actividad/importantes', views.filtrar_actividades_importantes, name='mostrar actividades importantes'),
    path('mostrar_actividad/no_importantes', views.filtrar_actividades_noimportantes, name='mostrar actividades no importantes'),
    path('profesores/', views.profesores, name='profesores'),
    path('asignar_materia_a_profesor/', views.asignar_materia_a_profesor, name='asignar materia a profesor'),
    path('registro/', views.registrarse, name='registro'),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar sesion'),
    path('planificacion/', views.planificacion, name='planificacion'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar sesion'),
    path('calendario/', views.calendario, name='calendario'),
    

]
