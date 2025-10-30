from django.db.models import Count
from collections import defaultdict
from apps.pdu.models import Pdu

REG_LIST = ['Nacional', 'Andes', 'Valles', 'Llanos']

def por_tipo():
    por_tipo = [
        {'modelo__marca__dispositivo': item['modelo__marca__dispositivo'] or 'Desconocido', 'total': item['total']}
        for item in Pdu.objects.values('modelo__marca__dispositivo').annotate(total=Count('id'))
    ]
    return por_tipo

def por_ciudad():
    por_ciudad = Pdu.objects.values('ubicacion__ciudad__nombre').annotate(total=Count('id')).order_by('-total')
    return por_ciudad

def por_regional():
    por_regional_depto = (
        Pdu.objects
        .values('regional__nombre', 'ubicacion__ciudad__nombre')
        .annotate(total=Count('id'))
        .order_by('regional__nombre', 'ubicacion__ciudad__nombre')
    )   

    # Reestructurar datos: {regional: {departamento: total}}
    datos = defaultdict(lambda: defaultdict(int))
    for item in por_regional_depto:
        reg = item['regional__nombre'] or 'Sin regional'
        dep = item['ubicacion__ciudad__nombre'] or 'Sin departamento'
        datos[reg][dep] = item['total']

    regionales = [r for r in REG_LIST if r in datos.keys()]
    departamentos = sorted({dep for d in datos.values() for dep in d.keys()})

    # Crear datasets para Chart.js
    datasets_regional = []
    for dep in departamentos:
        datasets_regional.append({
            'label': dep,
            'data': [datos[reg].get(dep, 0) for reg in regionales]
        })
    return regionales, datasets_regional

def dispositivos_administrables():
    adm_data_qs = (
        Pdu.objects
        .values('admin')
        .annotate(total=Count('id'))
        .order_by('admin')
    )

    adm_labels = ['Administrables' if item['admin'] else 'No Administrables' for item in adm_data_qs]
    adm_totals = [item['total'] for item in adm_data_qs]

    adm_data = {
        'labels': adm_labels,
        'totals': adm_totals
    }
    return adm_data

def dispositivos_adm_por_regional():
    adm_por_regional = (
        Pdu.objects.filter(admin=True)
        .values('regional__nombre', 'ubicacion__ciudad__nombre')
        .annotate(total=Count('id'))
        .order_by('regional__nombre', 'ubicacion__ciudad__nombre')
    )

    # Reestructurar datos: {regional: {departamento: total}}
    adm_datos = defaultdict(lambda: defaultdict(int))
    for item in adm_por_regional:
        reg = item['regional__nombre'] or 'Sin regional'
        dep = item['ubicacion__ciudad__nombre'] or 'Sin departamento'
        adm_datos[reg][dep] = item['total']

    # 🔹 Crear lista de regionales siguiendo el orden personalizado
    todas_regionales = list(adm_datos.keys())
    adm_regionales = [r for r in REG_LIST if r in todas_regionales] + [
        r for r in todas_regionales if r not in REG_LIST
    ]

    # 🔹 Obtener todos los departamentos únicos
    adm_departamentos = sorted({dep for d in adm_datos.values() for dep in d.keys()})

    # 🔹 Crear datasets para Chart.js
    adm_datasets_regional = []
    for dep in adm_departamentos:
        adm_datasets_regional.append({
            'label': dep,
            'data': [adm_datos[reg].get(dep, 0) for reg in adm_regionales]
        })

    # 🔹 Estructura final para el template
    adm_por_regional_chart = {
        'labels': adm_regionales,
        'datasets': adm_datasets_regional
    }
    
    return adm_por_regional_chart

def dispositivos_con_ip():
    adm_con_ip = Pdu.objects.filter(admin=True, ip__isnull=False).count()
    adm_sin_ip = Pdu.objects.filter(admin=True, ip__isnull=True).count()
    
    return {
        'labels': ['Registrados', 'No Registrados'],
        'totals': [adm_con_ip, adm_sin_ip]
    }