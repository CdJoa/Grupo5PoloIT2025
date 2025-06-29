from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.forms import modelformset_factory
from django.core.mail import send_mail
from django.http import JsonResponse
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_str
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from .models import Carrito
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.response import Response
from .serializers import CarritoSerializer
import json

from .models import *
from .forms import *

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
            user.email_verificado = False
            if user.generar_documento_unico():
                user.save()
                enviar_mail_verificacion(request, user)
                return render(request, 'verifica_tu_email.html', {'email': user.email})
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
def logout_view(request):
    logout(request)
    return redirect('home')

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
    usuario = request.user

    try:
        if not usuario.localidad:
            raise ValueError("Debes completar tu perfil con la localidad correspondiente antes de crear una mascota.")
        if not usuario.provincia:
            raise ValueError("Debes completar tu perfil con la provincia correspondiente antes de crear una mascota.")
        if not usuario.telefono:
            raise ValueError("Debes completar tu perfil con el teléfono correspondiente antes de crear una mascota.")
        if not usuario.documento:
            raise ValueError("Debes completar tu perfil con el documento correspondiente antes de crear una mascota.")
        if not usuario.email_verificado:
            raise ValueError("Debes verificar tu email antes de crear una mascota.")
    except ValueError as e:
        messages.error(request, str(e))
        return redirect('perfil_usuario')
    
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
            usuario.actualizar_mascotas_ids()
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
    mascota = get_object_or_404(Mascota, id=mascota_id)
    imagenes = mascota.imagenes.all()
    if request.method == 'POST' and request.user == mascota.duenio:
        imagen_id = request.POST.get('imagen_id')
        if imagen_id:
            mascota.imagenes.update(principal=False)
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
def solicitar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    if request.user == mascota.duenio:
        messages.error(request, "No puedes solicitar tu propia mascota.")
        return redirect('detalle_mascota', mascota_id=mascota_id)

    if request.method == 'POST':
        solicitud, created = SolicitudMascota.objects.get_or_create(
            mascota=mascota,
            solicitante=request.user,
            duenio=mascota.duenio
        )

        send_mail(
            subject='¡Tienes una nueva solicitud de adopción!',
            message=f'{request.user.username} quiere adoptar a {mascota.nombre}. Ingresa a tu perfil para ver los detalles y chatear.',
            from_email='matchpettest@gmail.com',
            recipient_list=[mascota.duenio.email],
            fail_silently=True,
        )

        messages.success(request, "Solicitud enviada al dueño de la mascota. Ahora puedes chatear con el dueño.")
        return redirect('chat_solicitud', solicitud_id=solicitud.id)

    return redirect('detalle_mascota', mascota_id=mascota_id)

@login_required
def chat_solicitud(request, solicitud_id):
    return render(request, 'chat.html', {'solicitud_id': solicitud_id})


@login_required
def mis_chats(request):
    solicitudes = SolicitudMascota.objects.filter(
        models.Q(solicitante=request.user) | models.Q(duenio=request.user)
    ).order_by('-fecha')
    return render(request, 'mis_chats.html', {'solicitudes': solicitudes})


@login_required
def solicitudes_recibidas(request):
    solicitudes = SolicitudMascota.objects.filter(
        duenio=request.user, estado='pendiente'
    )
    return render(request, 'solicitudes_recibidas.html', {'solicitudes': solicitudes})


@login_required
def responder_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudMascota, id=solicitud_id, duenio=request.user)
    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'aceptar':
            solicitud.estado = 'aceptada'
        elif accion == 'rechazar':
            solicitud.estado = 'rechazada'
        solicitud.save()
    return redirect('solicitudes_recibidas')


def base_context(request):
    tiene_mensajes_nuevos = SolicitudMascota.objects.filter(
        models.Q(duenio=request.user) | models.Q(solicitante=request.user),
    ).exists() if request.user.is_authenticated else False
    return {'tiene_mensajes_nuevos': tiene_mensajes_nuevos}


def enviar_mail_verificacion(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    link = request.build_absolute_uri(
        reverse('activar_cuenta', kwargs={'uidb64': uid, 'token': token})
    )
    send_mail(
        'Verifica tu email en PetMatch',
        f'Hola {user.username}, haz clic en el siguiente enlace para verificar tu email:\n{link}',
        'matchpettest@gmail.com',
        [user.email],
        fail_silently=False,
    )


def activar_cuenta(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Usuario.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.email_verificado = True
        user.save()
        messages.success(request, "¡Email verificado! Ya puedes iniciar sesión.")
        return redirect('login')
    else:
        return HttpResponse("Enlace de activación inválido o expirado.", status=400)


@login_required
def reenviar_verificacion(request):
    if request.method == 'POST' and not request.user.email_verificado:
        enviar_mail_verificacion(request, request.user)
        messages.success(request, "Te reenviamos el email de verificación.")
    return redirect('perfil_usuario')


@login_required(login_url='/api/no-autenticado/')
def carrito_api(request):
    usuario = request.user
    mascotas = Mascota.objects.filter(duenio=usuario)
    data = [
        {
            "id": m.id,
            "nombre": m.nombre,
            "descripcion": m.descripcion,
            "cantidad": 1,
            "imagen": m.imagenes.first().imagen.url if m.imagenes.exists() else ""
        }
        for m in mascotas
    ]
    return JsonResponse(data, safe=False)
#nuevo aporte
def no_autenticado_api(request):
    return JsonResponse({"error": "No estás autenticado"}, status=401)

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

@login_required
def ver_carrito(request):
    usuario = request.user
    carrito = Carrito.objects.filter(usuario=usuario)
    data = list(carrito.values())  # o usá un serializer si es DRF
    return JsonResponse(data, safe=False)

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
    
@api_view(['POST'])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    else:
        return Response({'error': 'Credenciales inválidas'}, status=401)
@permission_classes([IsAuthenticated])
def confirmar_adopcion(request):
    mascotas = request.data.get('mascotas', [])
    
    if not mascotas:
        return Response({"error": "No se enviaron mascotas."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Acá podrías guardar la adopción en una tabla si quisieras
    print("Usuario:", request.user.username)
    print("Mascotas seleccionadas:", mascotas)

    return Response({"mensaje": "Adopción registrada correctamente"}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def carrito_api(request):
    usuario = request.user
    mascotas = Mascota.objects.filter(duenio=usuario)
    data = [
        {
            "id": m.id,
            "nombre": m.nombre,
            "descripcion": m.descripcion,
            "cantidad": 1,
            "imagen": m.imagenes.first().imagen.url if m.imagenes.exists() else ""
        }
        for m in mascotas
    ]
    return Response(data)

@csrf_exempt  # Para que no pete si no tenés CSRF (pero mejor tenerlo)
def api_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # crea la sesión
            return JsonResponse({"message": "Login exitoso", "username": user.username})
        else:
            return JsonResponse({"error": "Credenciales inválidas"}, status=401)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)

class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer
    authentication_classes = [TokenAuthentication]  # acá
    permission_classes = [IsAuthenticated]