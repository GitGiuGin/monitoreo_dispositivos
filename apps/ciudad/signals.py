from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.ciudad.models import Ciudad

@receiver(post_migrate)
def crear_ciudades(sender, **kwargs):
    """
    Crea automáticamente las 9 ciudades (departamentos de Bolivia)
    después de migrar la base de datos.
    """
    if sender.label != "ciudad":
        return

    for nombre, _ in Ciudad.CHOISES_CIUDADES:
        Ciudad.objects.get_or_create(nombre=nombre)