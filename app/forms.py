from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.db import connection
class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'mail', 'password1', 'password2']
        
class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'edad', 'raza', 'castrado', 'descripcion']

class PerfilUsuarioForm(forms.ModelForm):
    provincia = forms.ModelChoiceField(
        queryset=Provincia.objects.none(),
        empty_label="Seleccioná una provincia",
        required=False
    )
    localidad = forms.ModelChoiceField(
        queryset=Localidad.objects.none(),
        empty_label="Seleccioná una localidad",
        required=False
    )

    class Meta:
        model = Usuario
        fields = ['mail', 'documento', 'telefono', 'provincia', 'localidad']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Mostrar vacío si el documento actual no es un número (=> lo consideramos artificial)
        if self.instance and self.instance.documento and not self.instance.documento.isdigit():
            self.initial['documento'] = ''

        self.fields['provincia'].queryset = Provincia.objects.all()
        provincia = None

        if 'provincia' in self.data:
            try:
                provincia_id = int(self.data.get('provincia'))
                provincia = Provincia.objects.get(id=provincia_id)
            except (ValueError, Provincia.DoesNotExist):
                pass
        elif self.instance and self.instance.provincia:
            provincia = self.instance.provincia

        if provincia:
            self.fields['localidad'].queryset = Localidad.objects.filter(id_provincia=provincia.id)
        else:
            self.fields['localidad'].queryset = Localidad.objects.none()

    def clean_documento(self):
        documento = self.cleaned_data.get('documento')
        if not documento:
            raise forms.ValidationError("El documento es obligatorio.")
        if not documento.isdigit():
            raise forms.ValidationError("Debe contener solo números.")
        existe = Usuario.objects.filter(documento=documento).exclude(pk=self.instance.pk).exists()
        if existe:
            raise forms.ValidationError("Este documento ya está registrado.")
        return documento

class MascotaImagenForm(forms.ModelForm):
    class Meta:
        model = MascotaImagen
        fields = ['imagen']

