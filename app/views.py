from django.shortcuts import render, redirect

from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User 
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.forms import modelformset_factory
from django.contrib.auth import logout


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        form = UsuarioForm()
        return render(request, 'signup.html', {'form': form})

    elif request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            for _ in range(10):  
                doc = get_random_string(length=8, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                if not Usuario.objects.filter(documento=doc).exists():
                    user.documento = doc
                    break
            else:
                form.add_error(None, "No se pudo generar un documento único. Intentá nuevamente.")
                return render(request, 'signup.html', {'form': form})

            user.save()
            login(request, user)
            return redirect('task')
        else:
            return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    elif request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Esto ahora sí llama a la función de Django
            return redirect('task')
        else:
            return HttpResponse("Error: Credenciales inválidas.", status=400)
        

@login_required
def perfil_usuario(request):
    usuario = request.user

    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Datos guardados correctamente.")

            return redirect('perfil_usuario')
    else:
        form = PerfilUsuarioForm(instance=usuario)

    mascotas = Mascota.objects.filter(duenio=usuario)
    return render(request, 'perfil.html', {
        'form': form,
        'user': usuario,
        'mascotas': mascotas,
    })

@login_required
def crear_mascota(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        imagenes = request.FILES.getlist('imagenes')
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.duenio = request.user
            mascota.save()
            # Guardar imágenes...
            for img in imagenes[:10]:
                MascotaImagen.objects.create(mascota=mascota, imagen=img)
            # ACTUALIZAR mascotas_ids del usuario
            request.user.actualizar_mascotas_ids()
            return redirect('perfil_usuario')
    else:
        form = MascotaForm()
    return render(request, 'crear_mascota.html', {'form': form})


def cargar_localidades(request):
    provincia_id = request.GET.get('provincia_id')
    localidades = Localidad.objects.filter(id_provincia=provincia_id).values('id', 'nombre')
    return JsonResponse(list(localidades), safe=False)


def task(request):
    if request.method == 'POST':
        # Aquí podrías manejar la lógica de la tarea
        return render(request, 'home.html', {"mensaje": "Tarea ejecutada correctamente."})
    else:
        return render(request, 'home.html', {"mensaje": "Método no permitido."})


def logout_view(request):
    logout(request)
    return redirect('home')  


def detalle_mascota(request, mascota_id):
    mascota = Mascota.objects.get(id=mascota_id)
    imagenes = mascota.imagenes.all()  # <--- Cambia esto
    if request.method == 'POST' and request.user == mascota.duenio:
        imagen_id = request.POST.get('imagen_id')
        if imagen_id:
            # Desmarcar todas
            mascota.imagenes_extra.update(principal=False)
            # Marcar la seleccionada
            MascotaImagen.objects.filter(id=imagen_id, mascota=mascota).update(principal=True)
            return redirect('detalle_mascota', mascota_id=mascota.id)
    return render(request, 'detalle_mascota.html', {
        'mascota': mascota,
        'imagenes': imagenes,
    })
