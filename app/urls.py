from django.urls import path
from django.contrib import admin  # 👈 Importa admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),  # 👈 Agrega el path para admin
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('task/', views.task, name='task'),
    path('logout/', views.logout_view, name='logout'),
    path('perros/', views.home, name='perros'),      # temporal, usa la vista home
    path('gatos/', views.home, name='gatos'),        # temporal, usa la vista home
    path('contacto/', views.home, name='contacto'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('ajax/cargar-localidades/', views.cargar_localidades, name='ajax_cargar_localidades'),
    path('mascotas/nueva/', views.crear_mascota, name='crear_mascota'),
    path('mascotas/<int:mascota_id>/', views.detalle_mascota, name='detalle_mascota'),
]