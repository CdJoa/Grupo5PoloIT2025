from django.contrib import admin
from .models import Mascota, SolicitudMascota, TraspasoMascota, MensajeChat

class MascotaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'duenio', 'estado')
    search_fields = ('nombre', 'duenio__username')

admin.site.register(Mascota, MascotaAdmin)
admin.site.register(SolicitudMascota)
admin.site.register(TraspasoMascota)
admin.site.register(MensajeChat)
