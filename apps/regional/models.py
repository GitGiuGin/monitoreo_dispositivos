from django.db import models

# Create your models here.
class Regional(models.Model):
    CHOICES_REGIONAL = [
    ('Nacional', 'Nacional'),
    ('Andes', 'Andes'),
    ('Llanos', 'Llanos'),
    ('Valles', 'Valles'),
    ]
    
    nombre = models.CharField(max_length=100, choices=CHOICES_REGIONAL)
                              
    class Meta:
        verbose_name = ("Regional")
        verbose_name_plural = ("Regionales")

    def __str__(self):
        return f"Regional: {self.nombre}"

