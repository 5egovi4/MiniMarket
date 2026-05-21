from django.db import models
from django.core.validators import MinValueValidator


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    precio = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    foto = models.ImageField(upload_to='productos/', blank=True, null=True)

    class Meta:
        db_table = 'producto'
