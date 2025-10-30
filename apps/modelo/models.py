from django.db import models
from apps.marca.models import Marca

# Create your models here.
class Modelo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, default=1, related_name='marcas')

    class Meta:
        verbose_name = ("Modelo")
        verbose_name_plural = ("Modelos")

    def __str__(self):
        return f"Modelo: {self.nombre} Marca: {self.marca.nombre}" 

