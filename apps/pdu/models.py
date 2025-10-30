from django.db import models
from apps.modelo.models import Modelo
from apps.ubicacion.models import Ubicacion
from apps.regional.models import Regional

# Create your models here.
class Pdu(models.Model):
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE, null=True, blank=True)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    regional = models.ForeignKey(Regional, on_delete=models.CASCADE)
    nfb = models.CharField(max_length=20, unique=True, null=True, blank=True)
    serie = models.CharField(max_length=50, unique=True, null=True, blank=True)
    ip = models.GenericIPAddressField(protocol='IPv4', unique=True, null=True, blank=True)
    usuario = models.CharField(max_length=50, null=True, blank=True)
    clave = models.CharField(max_length=50, null=True, blank=True)
    admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = ("Pdu")
        verbose_name_plural = ("Pdus")

    # def __str__(self):
    #     return self.marca.nombre + " - " + self.nfb

