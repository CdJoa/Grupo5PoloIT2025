from rest_framework import serializers
from .models import Carrito  # Importa tu modelo Carrito

class CarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrito
        fields = '__all__'  # Serializa todos los campos del modelo Carrito