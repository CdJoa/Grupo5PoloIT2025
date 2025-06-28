from django.urls import path, include
from django.contrib import admin  
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perros/', views.perros_view, name='perros'),
    path('gatos/', views.gatos_view, name='gatos'),  
    path('contacto/', views.contacto_view, name='contacto'),     
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('ajax/cargar-localidades/', views.cargar_localidades, name='ajax_cargar_localidades'),
    path('mascotas/nueva/', views.crear_mascota, name='crear_mascota'),
    path('mascotas/<int:mascota_id>/', views.detalle_mascota, name='detalle_mascota'),
    path('mascotas/<int:mascota_id>/solicitar/', views.solicitar_mascota, name='solicitar_mascota'),
    path('chat/<int:solicitud_id>/', views.chat_solicitud, name='chat_solicitud'),
    path('mensajes/', views.mis_chats, name='mis_chats'),
    path('solicitudes/', views.solicitudes_recibidas, name='solicitudes_recibidas'),
    path('solicitudes/<int:solicitud_id>/responder/', views.responder_solicitud, name='responder_solicitud'),
    path('activar/<uidb64>/<token>/', views.activar_cuenta, name='activar_cuenta'),
    path('reenviar-verificacion/', views.reenviar_verificacion, name='reenviar_verificacion'),


    # Reseteos de contraseña ya los maneja django por defecto
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]