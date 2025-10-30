from apps.modelo.models import Modelo
from django.shortcuts import get_object_or_404

def obtener_modelo(modelo_id):
    return get_object_or_404(Modelo, id=modelo_id)

def listar_modelos(nombre_marca='', nombre_modelo=''):
    modelos = Modelo.objects.all()
    if nombre_marca:
        modelos = modelos.filter(marca__nombre__icontains=nombre_marca)
    if nombre_modelo:
        modelos = modelos.filter(nombre__icontains=nombre_modelo)
            
    modelos = modelos.order_by('marca__nombre', 'nombre')
    return modelos

def crear_modelo(nombre, marca_id):
    modelo = Modelo(nombre=nombre, marca_id=marca_id)
    modelo.save()
    return modelo

def actualizar_modelo(modelo_id, nombre, marca_id):
    modelo = obtener_modelo(modelo_id)
    modelo.nombre = nombre
    modelo.marca_id = marca_id
    modelo.save()
    return modelo

def eliminar_modelo_controller(modelo_id):
    try:
        modelo = Modelo.objects.get(id=modelo_id)
        modelo.delete()
        return True
    except Modelo.DoesNotExist:
        return False
    
def modelo_existe(nombre, marca_id):
    modelo_existe = Modelo.objects.filter(nombre__iexact=nombre, marca_id=marca_id).exists()
    return modelo_existe

def modelo_existe_en_marca(nombre, modelo_id):
    return Modelo.objects.filter(nombre__iexact=nombre).exclude(id=modelo_id).exists()

def modelo_marca_existe(nombre, marca_id, modelo_id):
    return Modelo.objects.filter(nombre__iexact=nombre, marca_id=marca_id).exclude(id=modelo_id).exists()

def modelo_existe_global(nombre):
    return Modelo.objects.filter(nombre__iexact=nombre).exists()