from django.db import models

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    mail = models.EmailField(max_length=120, unique=True)

    class Meta:
        db_table = 'usuarios'     
        managed = False           
    def __str__(self):
        return f"{self.nombre} - {self.mail}"


class Mascota(models.Model):
    id = models.AutoField(primary_key=True)
    raza = models.CharField(max_length=100)
    localidad = models.CharField(max_length=100)
    duenio = models.ForeignKey(
        Usuario,
        on_delete=models.DO_NOTHING,
        db_column='duenio_id',
        related_name='mascotas'
    )

    class Meta:
        db_table = 'mascotas'     
        managed = False

    def __str__(self):
        return f"{self.raza} - {self.localidad}"
