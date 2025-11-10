from django.db import models

# Create your models here.
class Marca(models.Model):
    CHOISES_DISPOSITIVO = [
        ('PDU', 'PDU'),
        ('UPS', 'UPS'),
        ('SWITCH', 'SWITCH'),
        ('IMPRESORA', 'IMPRESORA'),
        ('AIRE ACONDICIONADO', 'AIRE ACONDICIONADO'),
        ('SERVIDOR', 'SERVIDOR')
    ]
    dispositivo = models.CharField(max_length=50, choices=CHOISES_DISPOSITIVO)
    nombre = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = ("Marca")
        verbose_name_plural = ("Marcas")

    def __str__(self):
        return F"Disp.: {self.dispositivo} Marca: {self.nombre}"