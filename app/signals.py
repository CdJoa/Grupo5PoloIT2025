from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Mascota

@receiver([post_save, post_delete], sender=Mascota)
def actualizar_mascotas_ids(sender, instance, **kwargs):
    usuario = instance.duenio
    ids = usuario.mascotas.values_list('id', flat=True)
    usuario.mascotas_ids = ','.join(str(i) for i in ids)
    usuario.save()