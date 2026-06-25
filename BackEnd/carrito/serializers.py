from rest_framework import serializers
from .models import Carrito
from productos.serializers import ProductoSerializer

class CarritoSerializer(serializers.ModelSerializer):
    id_producto = ProductoSerializer(read_only=True) # el serializer que manda Django a las cartas de productos
    id_producto_id = serializers.IntegerField(write_only=True) # el serializer que recibe Django para identificar un producto en la base de datos
    class Meta:
        model = Carrito
        fields = '__all__'
