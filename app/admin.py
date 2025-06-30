from django.contrib import admin
from .models import Mascota, SolicitudMascota, TraspasoMascota, MensajeChat, MensajeContacto, Usuario

class MascotaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'duenio', 'estado')
    search_fields = ('nombre', 'duenio__username')

class MensajeContactoPendienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'tema', 'mensaje', 'fecha', 'resuelto')
    search_fields = ('nombre', 'email', 'tema')
    list_filter = ('resuelto',)
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(resuelto=False)

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_active')
    search_fields = ('username', 'email')

    def delete_model(self, request, obj):
        obj.is_active = False
        obj.save()

admin.site.register(Mascota, MascotaAdmin)
admin.site.register(SolicitudMascota)
admin.site.register(MensajeContacto, MensajeContactoPendienteAdmin)
admin.site.register(Usuario, UsuarioAdmin)
