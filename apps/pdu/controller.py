from django.db.models import Q, Case, When, Count
from django.contrib import messages
from apps.pdu.models import Pdu


def listado_pdu():
    pdus = Pdu.objects.select_related('ubicacion', 'regional', 'modelo') \
        .order_by(
            Case(
                When(regional__nombre='Nacional', then=0),
                When(regional__nombre='Andes', then=1),
                When(regional__nombre='Llanos', then=2),
                When(regional__nombre='Valles', then=3),
            ),
            'ubicacion__ciudad__nombre',
            'ubicacion__tipo',
            'ubicacion__nombre'
        )
    return pdus

def crear_pdu_adm(modelo_id, ubicacion_id, regional_id, nfb, serie, ip, usuario, clave):
    return Pdu.objects.create(
        modelo_id=modelo_id,
        ubicacion_id=ubicacion_id,
        regional_id=regional_id,
        nfb=nfb or None,
        serie=serie or None,
        ip=ip or None,
        usuario=usuario or None,
        clave=clave or None,
        admin=True
    )
    
def crear_pdu_no_adm(ubicacion_id, regional_id):
    return Pdu.objects.create(
        ubicacion_id=ubicacion_id,
        regional_id=regional_id,
        admin=False
    )
    
def obtener_pdu(pdu_id):
    return Pdu.objects.get(id=pdu_id)

def validar_dublicados(nfb, serie, ip):
    duplicado = Pdu.objects.filter(
                    Q(nfb__iexact=nfb) | Q(serie__iexact=serie) | Q(ip__iexact=ip)
                ).first()
    return duplicado

def validar_dublicados_editar(pdu_id, nfb, serie, ip):
    duplicado = Pdu.objects.filter(
                    Q(nfb__iexact=nfb) | Q(serie__iexact=serie) | Q(ip__iexact=ip)
                ).exclude(id=pdu_id).first()
    return duplicado

def mensaje_error_duplicado(request, duplicado, nfb=None, serie=None, ip=None):
    if not duplicado:
        return False  # No hay duplicados

    campos_duplicados = []
    if duplicado.nfb and nfb and duplicado.nfb.lower() == nfb.lower():
        campos_duplicados.append(f"NFB={nfb}")
    if duplicado.serie and serie and duplicado.serie.lower() == serie.lower():
        campos_duplicados.append(f"Serie={serie}")
    if duplicado.ip and ip and duplicado.ip.lower() == ip.lower():
        campos_duplicados.append(f"IP={ip}")

    if campos_duplicados:
        mensaje = "Ya existe un dispositivo con " + ", ".join(campos_duplicados)
        messages.error(request, mensaje + ".")
        return True
    
    return False

# ----------- DASHBOARD -----------
def por_tipo():
    por_tipo = [
        {'modelo__marca__dispositivo': item['modelo__marca__dispositivo'] or 'Desconocido', 'total': item['total']}
        for item in Pdu.objects.values('modelo__marca__dispositivo').annotate(total=Count('id'))
    ]
    return por_tipo