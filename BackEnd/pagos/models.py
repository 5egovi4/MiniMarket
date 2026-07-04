from django.db import models
from pedido import models as pedido_models
from django.core.validators import MinValueValidator

class Pago(models.Model):
    ESTADOS = [
        ('Pago', 'Pago'),
        ('Pendiente', 'Pendiente'),
        ('Fallido', 'Fallido')
    ]

    id_pago = models.AutoField(primary_key=True)
    id_stripe = models.CharField(max_length=255, null=False)
    id_pedido = models.ForeignKey(pedido_models.Pedido, models.PROTECT)
    estado_pago = models.CharField(max_length=10, choices=ESTADOS)
    metodo_pago = models.CharField(max_length=45, null=False)
    total = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(0)])
    fecha_pago = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'pagos'