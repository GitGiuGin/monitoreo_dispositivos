from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.regional.models import Regional

@receiver(post_migrate)
def crear_regionales(sender, **kwargs):
    """
    Crea automáticamente las regionales (Nacional, Andes, Valles, Llanos)
    después de migrar la base de datos.
    """
    if sender.label != "regional":  # solo ejecuta cuando la app regional migra
        return

    for nombre, _ in Regional.CHOICES_REGIONAL:
        Regional.objects.get_or_create(nombre=nombre)
