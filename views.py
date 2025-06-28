from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, Http404
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.forms import modelformset_factory
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    form = BusquedaMascotaForm(request.GET or None)
    mascotas = Mascota.objects.filter(disponible=True)

    if form.is_valid():
        especie = form.cleaned_data.get('especie')
        provincia = form.cleaned_data.get('provincia')
        localidad = form.cleaned_data.get('localidad')
        castrado = form.cleaned_data.get('castrado')

        if especie:
            mascotas = mascotas.filter(especie=especie)
        if provincia:
            mascotas = mascotas.filter(provincia=provincia)
        if localidad:
            mascotas = mascotas.filter(localidad=localidad)
        if castrado is not None:
            mascotas = mascotas.filter(castrado=castrado)

    return render(request, 'home.html', {
        'form': form,
        'mascotas': mascotas,
    })



def signup(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if user.generar_documento_unico():
                user.save()
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "No se pudo generar un documento único.")
    else:
        form = UsuarioForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    elif request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  
            return redirect('home')
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
            mascota.provincia = request.user.provincia
            mascota.localidad = request.user.localidad
            mascota.save()
            for img in imagenes[:10]: 
                MascotaImagen.objects.create(mascota=mascota, imagen=img)
            request.user.actualizar_mascotas_ids()
            return redirect('perfil_usuario')
    else:
        form = MascotaForm()
    return render(request, 'crear_mascota.html', {'form': form})


def cargar_localidades(request):
    provincia_id = request.GET.get('provincia_id')
    localidades = Localidad.objects.filter(id_provincia=provincia_id).values('id', 'nombre')
    return JsonResponse(list(localidades), safe=False)

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')  


def detalle_mascota(request, mascota_id):
    mascota = Mascota.objects.get(id=mascota_id)
    imagenes = mascota.imagenes.all() 
    if request.method == 'POST' and request.user == mascota.duenio:
        imagen_id = request.POST.get('imagen_id')
        if imagen_id:
            mascota.imagenes_extra.update(principal=False)
            MascotaImagen.objects.filter(id=imagen_id, mascota=mascota).update(principal=True)
            return redirect('detalle_mascota', mascota_id=mascota.id)
    return render(request, 'detalle_mascota.html', {
        'mascota': mascota,
        'imagenes': imagenes,
    })



def mascotas_por_especie_view(request, especie, template_name):
    form = BusquedaMascotaForm(request.GET or None)
    mascotas = Mascota.objects.filter(disponible=True, especie=especie)

    if form.is_valid():
        provincia = form.cleaned_data.get('provincia')
        localidad = form.cleaned_data.get('localidad')
        castrado = form.cleaned_data.get('castrado')

        if provincia:
            mascotas = mascotas.filter(provincia=provincia)
        if localidad:
            mascotas = mascotas.filter(localidad=localidad)
        if castrado is not None:
            mascotas = mascotas.filter(castrado=castrado)

    return render(request, template_name, {
        'form': form,
        'mascotas': mascotas,
    })

def perros_view(request):
    return mascotas_por_especie_view(request, especie='perro', template_name='perros.html')

def gatos_view(request):
    return mascotas_por_especie_view(request, especie='gato', template_name='gatos.html')

def contacto_view(request):
    return render(request, 'contacto.html')

@login_required
def carrito_api(request):
    usuario = request.user

    # Ejemplo simple: todas las mascotas que le pertenecen al usuario
    mascotas = Mascota.objects.filter(duenio=usuario)

    data = []
    for m in mascotas:
        data.append({
            "id": m.id,
            "nombre": m.nombre,
            "descripcion": m.descripcion,
            
            "cantidad": 1,
            "imagen": m.imagenes.first().imagen.url if m.imagenes.exists() else ""
        })

    return JsonResponse(data, safe=False)
#nuevo aporte
def mascotas_api(request):
    mascotas = Mascota.objects.filter(disponible=True)

    data = []
    for m in mascotas:
        data.append({
            "id": m.id,
            "nombre": m.nombre,
            "descripcion": m.descripcion,
            "especie": m.especie,
            "provincia": m.provincia.nombre if m.provincia else "",
            "localidad": m.localidad.nombre if m.localidad else "",
            
            "imagen": m.imagenes.first().imagen.url if m.imagenes.exists() else "",
        })
    
    return JsonResponse(data, safe=False)

@csrf_exempt
def api_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login exitoso", "username": user.username})
        else:
            return JsonResponse({"error": "Credenciales inválidas"}, status=401)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)

def mascota_detalle_api(request, mascota_id):
    try:
        m = Mascota.objects.get(id=mascota_id, disponible=True)
        data = {
            "id": m.id,
            "nombre": m.nombre,
            "descripcion": m.descripcion,
            "especie": m.especie,
            "provincia": m.provincia.nombre if m.provincia else "",
            "localidad": m.localidad.nombre if m.localidad else "",
            "imagen": m.imagenes.first().imagen.url if m.imagenes.exists() else "",
        }
        return JsonResponse(data)
    except Mascota.DoesNotExist:
        raise Http404("Mascota no encontrada")