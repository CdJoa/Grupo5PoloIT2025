from django.shortcuts import render, redirect , get_object_or_404

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
from django.core.mail import send_mail


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
            mascota.duenio = usuario
            mascota.provincia = usuario.provincia
            mascota.localidad = usuario.localidad
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
    mascotas = Mascota.objects.filter(disponible=True, especie=especie, estado='esperando')

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
    form = ContactoForm()
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.resuelto = False  # fuerza el valor
            mensaje.save()
            messages.success(request, "¡Mensaje enviado!")
            return redirect('home')
    return render(request, 'contacto.html', {'form': form})


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

        messages.success(request, "Solicitud enviada al dueño de la mascota. Ahora puedes ver el estado en tu bandeja de chats.")
        return redirect('mis_chats')  
    return redirect('detalle_mascota', mascota_id=mascota_id)

def base_context(request):
    tiene_mensajes_nuevos = SolicitudMascota.objects.filter(
        models.Q(duenio=request.user) | models.Q(solicitante=request.user),
    ).exists() if request.user.is_authenticated else False
    return {'tiene_mensajes_nuevos': tiene_mensajes_nuevos}


@login_required
def chat_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudMascota, id=solicitud_id)
    mensajes = MensajeChat.objects.filter(solicitud=solicitud).order_by('fecha')
    existe_traspaso = TraspasoMascota.objects.filter(
        mascota=solicitud.mascota,
        duenio_anterior=solicitud.duenio,
        duenio_nuevo=solicitud.solicitante,
        estado='esperando'
    ).exists()

    if request.method == 'POST' and 'mensaje' in request.POST:
        texto = request.POST.get('mensaje')
        if texto:
            MensajeChat.objects.create(
                solicitud=solicitud,
                usuario=request.user, 
                texto=texto
            )
        return redirect('chat_solicitud', solicitud_id=solicitud_id)

    return render(request, 'chat.html', {
        'solicitud': solicitud,
        'mensajes': mensajes,
        'existe_traspaso': existe_traspaso,
    })

@login_required
def mis_chats(request):
    solicitudes = SolicitudMascota.objects.filter(
        (models.Q(solicitante=request.user) | models.Q(duenio=request.user)) &
        ~models.Q(estado="rechazada")
    ).order_by('-fecha')
    return render(request, 'mis_chats.html', {'solicitudes': solicitudes})


@login_required
def responder_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudMascota, id=solicitud_id, duenio=request.user)
    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'aceptar':
            solicitud.estado = 'aceptada'
            solicitud.save()
            messages.success(request, "Solicitud aceptada. Ahora puedes chatear con el adoptante.")
            return redirect('chat_solicitud', solicitud_id=solicitud.id) 
        elif accion == 'rechazar':
            solicitud.estado = 'rechazada'
            solicitud.save()
            messages.info(request, "Solicitud rechazada.")
        return redirect('mis_chats')
    return render(request, 'responder_solicitud.html', {'solicitud': solicitud})


from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator

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

from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages

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

@login_required
def enviar_traspaso(request, solicitud_id):
    try:
        solicitud = get_object_or_404(SolicitudMascota, id=solicitud_id, duenio=request.user, estado='aceptada')
        if request.method == 'POST':
            traspaso = TraspasoMascota.objects.filter(
                mascota=solicitud.mascota,
                duenio_anterior=request.user,
                duenio_nuevo=solicitud.solicitante
            ).order_by('-fecha').first()
            if traspaso and traspaso.estado == 'esperando':
                messages.info(request, "Ya existe una solicitud de traspaso pendiente para esta mascota.")
            elif traspaso and traspaso.estado == 'rechazada':
                traspaso.estado = 'esperando'
                traspaso.save()
                messages.success(request, "Solicitud de traspaso reenviada.")
            else:
                TraspasoMascota.objects.create(
                    mascota=solicitud.mascota,
                    duenio_anterior=request.user,
                    duenio_nuevo=solicitud.solicitante,
                    estado='esperando'
                )
                messages.success(request, "Solicitud de traspaso enviada.")
    except Exception as e:
        messages.error(request, f"Ocurrió un error al enviar el traspaso: {str(e)}")
    return redirect('chat_solicitud', solicitud_id=solicitud_id)

@login_required
def responder_traspaso(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudMascota, id=solicitud_id, solicitante=request.user)
    traspaso = TraspasoMascota.objects.filter(
        mascota=solicitud.mascota,
        duenio_anterior=solicitud.duenio,
        duenio_nuevo=request.user,
        estado='esperando'
    ).first()
    if request.method == 'POST' and traspaso:
        accion = request.POST.get('accion')
        if accion == 'aceptar':
            traspaso.estado = 'aceptada'
            traspaso.save()
            solicitud.mascota.cambiar_duenio(request.user)
            solicitud.mascota.estado = 'adoptado'  
            solicitud.mascota.save()
            messages.success(request, "¡Has aceptado el traspaso! Ahora eres el dueño de la mascota.")
        elif accion == 'rechazar':
            traspaso.estado = 'rechazada'
            traspaso.save()
            messages.info(request, "Has rechazado el traspaso.")
    return redirect('chat_solicitud', solicitud_id=solicitud_id)

@login_required
def cancelar_traspaso(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudMascota, id=solicitud_id, duenio=request.user)
    traspaso = TraspasoMascota.objects.filter(
        mascota=solicitud.mascota,
        duenio_anterior=request.user,
        duenio_nuevo=solicitud.solicitante,
        estado='esperando'
    ).first()
    if request.method == 'POST' and traspaso:
        traspaso.delete()
        messages.success(request, "Solicitud de traspaso cancelada.")
    return redirect('chat_solicitud', solicitud_id=solicitud_id)

