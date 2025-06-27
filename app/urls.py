from django.urls import path
from django.contrib import admin  
from . import views

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
]