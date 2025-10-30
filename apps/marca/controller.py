from apps.marca.models import Marca

def listar_marcas(nombre=''):
    marcas = Marca.objects.all()
    if nombre:
        marcas = marcas.filter(nombre__icontains=nombre)
    return marcas

def crear_marca(dispositivo, nombre):
    marca = Marca(dispositivo=dispositivo, nombre=nombre)
    marca.save()
    return marca

def listar_dispositivos():
    return [{"valor": valor, "nombre": nombre} for valor, nombre in Marca.CHOISES_DISPOSITIVO]

def marca_existe(dispositivo, nombre):
    marca_existe = Marca.objects.filter(dispositivo=dispositivo, nombre__iexact=nombre).exists()
    return marca_existe