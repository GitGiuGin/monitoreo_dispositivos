from apps.ciudad.models import Ciudad
from django.db.models import Min

def listar_ciudad():
    return Ciudad.objects.all()

def obtener_ciudad_id(ciudad_id):
    return Ciudad.objects.get(id=ciudad_id)