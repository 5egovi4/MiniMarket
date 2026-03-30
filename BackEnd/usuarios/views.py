from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Usuario
from .serializers import UsuarioSerializer
from datetime import date

@api_view(['POST'])
def registrar_usuario(request):
    data = request.data.copy()
    data['fecha_registro'] = date.today()
    serializer = UsuarioSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_usuario(request):
    email = request.data.get('email')
    contraseña = request.data.get('contraseña')

    if not email or not contraseña:
        return Response({'error': 'Email y contraseña son requeridos'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        usuario = Usuario.objects.get(email=email)
    except Usuario.DoesNotExist:
        return Response({'error': 'Credenciales incorrectas'}, status=status.HTTP_401_UNAUTHORIZED)

    if usuario.contraseña != contraseña:
        return Response({'error': 'Credenciales incorrectas'}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = UsuarioSerializer(usuario)
    return Response({
        'mensaje': 'Login exitoso',
        'usuario': serializer.data
    })

@api_view(['GET'])
def obtener_usuario(request, id):
    try:
        usuario = Usuario.objects.get(pk=id)
    except Usuario.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)

@api_view(['PUT'])
def actualizar_usuario(request, id):
    try:
        usuario = Usuario.objects.get(pk=id)
    except Usuario.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def eliminar_usuario(request, id):
    try:
        usuario = Usuario.objects.get(pk=id)
    except Usuario.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    usuario.delete()
    return Response({'mensaje': 'Cuenta eliminada correctamente'}, status=status.HTTP_204_NO_CONTENT)