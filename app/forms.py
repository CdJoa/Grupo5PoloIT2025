from django import forms
from .models import Usuario, Mascota

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'mail']

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['raza', 'localidad', 'duenio']
