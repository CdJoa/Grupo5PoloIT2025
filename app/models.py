# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
import random, string

class Usuario(AbstractUser):
    telefono = models.CharField(max_length=20, blank=True, default='')
    documento = models.CharField(max_length=20, unique=True)
    provincia = models.ForeignKey('Provincia', on_delete=models.SET_NULL, null=True, db_column='provincia_id')
    localidad = models.ForeignKey('Localidad', on_delete=models.SET_NULL, null=True, db_column='localidad_id')
    mascotas_ids = models.CharField(max_length=255, blank=True, default='', db_column='mascotas_ids')
    email = models.EmailField()

    email_verificado = models.BooleanField(default=False)
    class Meta:
        db_table = 'usuarios'
        managed = False  
    def __str__(self):
        return self.username

    def set_mascotas_ids(self, ids):
        self.mascotas_ids = ','.join(str(i) for i in ids)

    def get_mascotas_ids(self):
        if self.mascotas_ids:
            return [int(i) for i in self.mascotas_ids.split(',') if i]
        return []
    def clean_documento(self):
        documento = self.cleaned_data.get('documento')
        if not documento:
            raise forms.ValidationError("El documento es obligatorio.")
        if not documento.isdigit():
            raise forms.ValidationError("El documento debe contener solo números.")
        existe = Usuario.objects.filter(documento=documento).exclude(pk=self.instance.pk).exists()
        if existe:
            raise forms.ValidationError("Este documento ya está registrado.")
        return documento
    
    def generar_documento_unico(self):
        for _ in range(10):
            doc = ''.join(random.choices(string.ascii_uppercase, k=8))
            if not Usuario.objects.filter(documento=doc).exists():
                self.documento = doc
                return True
        return False

    def actualizar_mascotas_ids(self):
        ids = self.mascotas.values_list('id', flat=True)
        self.mascotas_ids = ','.join(str(i) for i in ids)
        self.save()

class Provincia(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'provincias'
        managed = False

    def __str__(self):
        return self.nombre

class Localidad(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    id_provincia = models.IntegerField()  
    class Meta:
        db_table = 'localidades'
        managed = False

    def __str__(self):
        return self.nombre

class Mascota(models.Model):
    ESPECIE_CHOICES = [
        ('perro', 'Perro'),
        ('gato', 'Gato'),
    ]
            # 'perro' se guarda en la base de datos 
            # 'Perro' se muestra en el formulario 
    EDAD_CHOICES = [
        ('cachorro', 'Cachorro'),
        ('adulto', 'Adulto'),
        ('senior', 'Senior'),
    ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=10, choices=ESPECIE_CHOICES)
    edad = models.CharField(max_length=10, choices=EDAD_CHOICES)
    raza = models.CharField(max_length=100)
    localidad = models.ForeignKey(
        Localidad,
        on_delete=models.SET_NULL,
        null=True,
        db_column='localidad_id'
    )
    provincia = models.ForeignKey(
        Provincia,
        on_delete=models.SET_NULL,
        null=True,
        db_column='provincia_id'
    )
    duenio = models.ForeignKey(
        Usuario,
        on_delete=models.DO_NOTHING,
        db_column='duenio_id',
        related_name='mascotas'
    )
    castrado = models.BooleanField(default=False)
    descripcion = models.TextField(blank=True)
    disponible = models.BooleanField(default=True)  

    class Meta:
        db_table = 'mascotas'
        managed = False  
    def __str__(self):
        return f"{self.especie} - {self.raza} ({self.edad})"

class MascotaImagen(models.Model):
    mascota = models.ForeignKey(Mascota, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='mascotas/')
    principal = models.BooleanField(default=False)

    class Meta:
        db_table = 'mascota_imagenes'  
        managed = False

class SolicitudMascota(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='solicitudes')
    solicitante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='solicitudes_enviadas')
    duenio = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='solicitudes_recibidas')
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='pendiente') 

    class Meta:
        db_table = 'solicitudes_mascota'
        managed = False

    def __str__(self):
        return f"{self.solicitante} → {self.mascota} ({self.estado})"
