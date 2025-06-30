# forms.py
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']
        
class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'edad', 'raza', 'castrado', 'descripcion']

class MascotaImagenForm(forms.ModelForm):
    class Meta:
        model = MascotaImagen
        fields = ['imagen']

def get_localidades_queryset_from_data(data, initial=None):
    provincia = None
    if data and 'provincia' in data:
        try:
            provincia_id = int(data.get('provincia'))
            provincia = Provincia.objects.get(id=provincia_id)
        except (ValueError, Provincia.DoesNotExist):
            provincia = None
    elif initial:
        provincia = initial

    if provincia:
        return Localidad.objects.filter(id_provincia=provincia.id)
    else:
        return Localidad.objects.none()

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
        fields = ['email', 'documento', 'telefono', 'provincia', 'localidad']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.documento and not self.instance.documento.isdigit():
            self.initial['documento'] = ''

        self.fields['provincia'].queryset = Provincia.objects.all()
        self.fields['localidad'].queryset = get_localidades_queryset_from_data(
            self.data,
            initial=self.instance.provincia if self.instance else None
        )

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

class BusquedaMascotaForm(forms.Form):
    especie = forms.ChoiceField(
        choices=[('', 'Todos'), ('perro', 'Perro'), ('gato', 'Gato')],
        required=False,
        label='Especie'
    )
    provincia = forms.ModelChoiceField(
        queryset=Provincia.objects.all(),
        required=False,
        empty_label="Todas las provincias"
    )
    localidad = forms.ModelChoiceField(
        queryset=Localidad.objects.none(),
        required=False,
        empty_label="Todas las localidades"
    )
    castrado = forms.NullBooleanField(
        required=False,
        label='Castrado',
        widget=forms.Select(choices=[('', 'Todos'), ('True', 'Sí'), ('False', 'No')])
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['localidad'].queryset = get_localidades_queryset_from_data(self.data)
