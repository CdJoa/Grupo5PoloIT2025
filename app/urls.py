from django.urls import path, include
from django.contrib import admin  
from . import views
from django.contrib.auth import views as auth_views
from rest_framework import routers
from .views import CarritoViewSet
from .views import confirmar_adopcion
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'carrito', CarritoViewSet)

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

    # Rutas API REST
    path('api/carrito/', views.carrito_api, name='carrito_api'),
    path('api/pets/', views.mascotas_api, name='mascotas_api'),
    path('api/login/', views.api_login, name='api_login'),
    path('api/pets/<int:mascota_id>/', views.mascota_detalle_api, name='mascota_detalle_api'),
    path('api/adopcion/', confirmar_adopcion),
    path('api/no-autenticado/', views.no_autenticado_api, name='no_autenticado_api'),
    path('api/', include(router.urls)),

    # Rutas de solicitudes y chat
    path('mascotas/<int:mascota_id>/solicitar/', views.solicitar_mascota, name='solicitar_mascota'),
    path('chat/<int:solicitud_id>/', views.chat_solicitud, name='chat_solicitud'),
    path('chat/', views.lista_chats, name='lista_chats'),
    path('mensajes/', views.mis_chats, name='mis_chats'),
    path('solicitudes/', views.solicitudes_recibidas, name='solicitudes_recibidas'),
    path('solicitudes/<int:solicitud_id>/responder/', views.responder_solicitud, name='responder_solicitud'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('mascotas/', views.mascotas_view, name='mascotas'),
    
    # Activación y verificación
    path('activar/<uidb64>/<token>/', views.activar_cuenta, name='activar_cuenta'),
    path('reenviar-verificacion/', views.reenviar_verificacion, name='reenviar_verificacion'),

    # Reset de contraseña (Django auth views)
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    # Rutas de traspaso (del otro lado)
    path('traspaso/<int:solicitud_id>/enviar/', views.enviar_traspaso, name='enviar_traspaso'),
    path('traspaso/<int:solicitud_id>/responder/', views.responder_traspaso, name='responder_traspaso'),
    path('traspaso/<int:solicitud_id>/cancelar/', views.cancelar_traspaso, name='cancelar_traspaso'),
    
]
