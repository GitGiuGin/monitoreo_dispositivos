from django.db import models
from apps.ciudad.models import Ciudad

# Create your models here.
class Ubicacion(models.Model):
    CHOICES_TIPO = [
        ('Oficina Nacional', 'Oficina Nacional'),
        ('Sucursal', 'Sucursal'),
        ('Agencia', 'Agencia'),
    ]
    
    tipo = models.CharField(max_length=100, choices=CHOICES_TIPO)
    nombre = models.CharField(max_length=100) # Nombre de la ubicación
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = ("Ubicacion")
        verbose_name_plural = ("Ubicaciones")

    def __str__(self):
        return f"{self.nombre} - {self.ciudad.nombre}"