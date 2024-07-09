from django.shortcuts import render, redirect
from .forms import CrearActividad

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
            return redirect('/')