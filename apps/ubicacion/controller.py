# apps/ubicacion/controllers.py
from apps.ubicacion.models import Ubicacion

def crear_ubicacion(tipo, nombre, ciudad_id=None):
    return Ubicacion.objects.create(
        tipo=tipo,
        nombre=nombre,
        ciudad_id=ciudad_id
    )

def listar_ubicaciones():
    """
    Retorna todas las ubicaciones.
    """
    return Ubicacion.objects.select_related("ciudad").all()

def obtener_ubicacion(ubicacion_id):
    """
    Retorna una ubicación específica.
    """
    try:
        return Ubicacion.objects.select_related("ciudad").get(id=ubicacion_id)
    except Ubicacion.DoesNotExist:
        return None

def listar_tipos():
    return [{"valor": valor, "nombre": nombre} for valor, nombre in Ubicacion.CHOICES_TIPO]

def eliminar_ubicacion(ubicacion_id):
    ubicacion = Ubicacion.objects.get(id=ubicacion_id)
    if ubicacion:
        ubicacion.delete()
        return True
    return False