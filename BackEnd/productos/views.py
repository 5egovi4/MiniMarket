from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Producto
from .serializers import ProductoSerializer 

@api_view(['GET'])
def listar_productos(request):
    productos = Producto.objects.all()
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def obtener_producto(request, id):
    try:
        producto = Producto.objects.get(pk=id)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProductoSerializer(producto)
    return Response(serializer.data)

@api_view(['POST'])
def agregar_producto(request):
    serializer = ProductoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def actualizar_producto(request, id):
    try:
        producto = Producto.objects.get(pk=id)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProductoSerializer(producto, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def eliminar_producto(request, id):
    try:
        producto = Producto.objects.get(pk=id)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    producto.delete()
    return Response({'mensaje': 'Producto eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)