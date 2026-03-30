from django.db import models

class Usuario(models.Model):
    ROL_CHOICES = [
        ('admin', 'Admin'),
        ('cliente', 'Cliente'),
    ]

    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    email = models.EmailField(max_length=100, unique=True)
    contraseña = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    num_telefono = models.CharField(max_length=15, blank=True, null=True)
    tarjeta_credito = models.CharField(max_length=16, blank=True, null=True)
    fecha_registro = models.DateField()
    rol = models.CharField(max_length=10, choices=ROL_CHOICES)

    class Meta:
        db_table = 'usuario'