from django.db import models
from usuarios import models as model_usuario
from productos import models as model_producto
from django.core.validators import MinValueValidator

class Carrito(models.Model):
    id_carrito = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(model_usuario.Usuario, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(model_producto.Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        db_table = 'carro_compras' 
