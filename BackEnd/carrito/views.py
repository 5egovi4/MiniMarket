from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Carrito
from usuarios import models as usuario_model 
from productos import models as producto_model
from .serializers import CarritoSerializer

@api_view(['POST'])
def agregar_producto(request):
    id_usuario = request.data.get('id_usuario')
    id_producto = request.data.get('id_producto_id')
    cantidad_solicitada = request.data.get('cantidad')

    try:
        usuario = usuario_model.Usuario.objects.get(pk=id_usuario)
    except usuario_model.Usuario.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        producto = producto_model.Producto.objects.get(pk=id_producto)
    except producto_model.Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if producto.stock < cantidad_solicitada:
        return Response({'error': 'Stock insuficiente'}, status=status.HTTP_400_BAD_REQUEST)

    existencia = Carrito.objects.filter(id_usuario=id_usuario, id_producto=id_producto).first()

    if existencia:
        cantidad = existencia.cantidad + request.data.get('cantidad')
        existencia.cantidad = cantidad
        existencia.save()
        return Response({'Mensaje':'Carrito actualizado'}, status=status.HTTP_200_OK)
    else:
        serializer = CarritoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
def ver_carrito(request, id):
    try:
        usuario = usuario_model.Usuario.objects.get(pk=id)
    except usuario_model.Usuario.DoesNotExist:
        return Response({'Error':'Usario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    productos = Carrito.objects.filter(id_usuario=id)
    serializer = CarritoSerializer(productos, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def eliminar_producto(request, id_usuario, id_producto):
    try:
        producto = Carrito.objects.get(id_producto=id_producto, id_usuario=id_usuario)
    except Carrito.DoesNotExist:
        return Response({'Error':'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    producto.delete()
    return Response({'Mensaje':'Producto eliminado del carrito'}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def vaciar_carrito(request, id_usuario):
    carrito = Carrito.objects.filter(id_usuario=id_usuario)
    if not carrito.exists():
        return Response({'Mensaje':'El usuario no tiene productos en el carrito'}, status=status.HTTP_404_NOT_FOUND)
    
    carrito.delete()
    return Response({'Mensaje':'Carrito vaciado'}, status=status.HTTP_200_OK)