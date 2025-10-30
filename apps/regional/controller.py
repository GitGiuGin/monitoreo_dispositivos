from apps.regional.models import Regional
from apps.ciudad.controller import obtener_ciudad_id

def listar_regionales():
    return Regional.objects.all()

def asignar_regional(tipo, ciudad_id):
    if tipo == "Oficina Nacional" and ciudad_id == 1:
        return 1
    else:
        ciudad = obtener_ciudad_id(ciudad_id)
        nombre = ciudad.nombre

        mapa = {
            "La Paz": 2,
            "Oruro": 2,
            "Potosi": 2,
            "Pando": 2,
            "Beni": 3,
            "Santa Cruz": 3,
            "Cochabamba": 4,
            "Chuquisaca": 4,
            "Tarija": 4,
        }
        return mapa.get(nombre)