from django.db import models

# Create your models here.
class Ciudad(models.Model):
    CHOISES_CIUDADES = [
        ('La Paz', 'La Paz'),
        ('Cochabamba', 'Cochabamba'),
        ('Santa Cruz', 'Santa Cruz'),
        ('Oruro', 'Oruro'),
        ('Potosi', 'Potosí'),
        ('Chuquisaca', 'Chuquisaca'),
        ('Tarija', 'Tarija'),
        ('Beni', 'Beni'),
        ('Pando', 'Pando'),
    ]
    
    nombre = models.CharField(max_length=100, unique=True, choices=CHOISES_CIUDADES)

    class Meta:
        verbose_name = ("Ciudad")
        verbose_name_plural = ("Ciudades")

    def __str__(self):
        return f"Ciudad: {self.nombre}"
