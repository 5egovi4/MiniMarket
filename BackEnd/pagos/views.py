from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import stripe
import json
import os
from dotenv import load_dotenv

from carrito.models import Carrito
from pedido.models import Pedido, DetallePedido
from usuarios.models import Usuario
from pagos.utils import calcular_total


load_dotenv()
stripe.api_key = os.getenv('STRIPE_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')



@api_view(['POST'])
def crear_payment_intent(request):
    id_usuario = request.data.get('id_usuario')
    direccion_envio = request.data.get('direccion_envio')

    if not id_usuario or not direccion_envio:
        return Response({'error': 'id_usuario y direccion_envio son requeridos'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        usuario = Usuario.objects.get(pk=id_usuario)
    except Usuario.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    total = calcular_total(id_usuario)

    if total <= 0:
        return Response({'error': 'El carrito está vacío'}, status=status.HTTP_400_BAD_REQUEST)

    intent = stripe.PaymentIntent.create(
        amount=int(total * 100),
        currency='usd',
        metadata={
            'id_usuario': id_usuario,
            'direccion_envio': direccion_envio,
        }
    )

    return Response({
        'client_secret': intent.client_secret,
        'total': total,
    })


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        id_usuario = intent['metadata']['id_usuario']
        direccion_envio = intent['metadata']['direccion_envio']
        stripe_id = intent['id']
        total = intent['amount'] / 100

        try:
            usuario = Usuario.objects.get(pk=id_usuario)
            items = Carrito.objects.filter(id_usuario=id_usuario)

            pedido = Pedido.objects.create(
                id_usuario=usuario,
                total=total,
                metodo_pago='tarjeta',
                estado_pago='completado',
                direccion_envio=direccion_envio,
                stripe_id=stripe_id,
            )

            for item in items:
                DetallePedido.objects.create(
                    id_pedido=pedido,
                    id_producto=item.id_producto,
                    cantidad=item.cantidad,
                    precio_unitario=item.id_producto.precio,
                )
                # reducir stock
                producto = item.id_producto
                producto.stock -= item.cantidad
                producto.save()

            # vaciar carrito
            items.delete()

        except Exception as e:
            return HttpResponse(status=500)

    return HttpResponse(status=200)