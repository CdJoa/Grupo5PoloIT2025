from django.shortcuts import render, redirect
from .models import Usuario, Mascota
from .forms import UsuarioForm, MascotaForm

def home(request):
    return render(request, 'home.html')

def listar_usuarios(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('usuarios')
    else:
        form = UsuarioForm()

    usuarios = Usuario.objects.all()
    return render(request, 'usuarios.html', {'form': form, 'usuarios': usuarios})

def listar_mascotas(request):
    if request.method == "POST":
        form = MascotaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mascotas')
    else:
        form = MascotaForm()

    mascotas = Mascota.objects.select_related('duenio').all()
    return render(request, 'mascotas.html', {'form': form, 'mascotas': mascotas})
