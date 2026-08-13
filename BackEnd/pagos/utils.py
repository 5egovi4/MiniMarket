from carrito.models import Carrito

def calcular_total(id_usuario):
    items = Carrito.objects.filter(id_usuario=id_usuario)
    total = 0
    for item in items:
        total += item.id_producto.precio * item.cantidad
    return total
