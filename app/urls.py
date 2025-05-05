# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('usuarios/', views.listar_usuarios, name='usuarios'),
    path('mascotas/', views.listar_mascotas, name='mascotas'),
]
