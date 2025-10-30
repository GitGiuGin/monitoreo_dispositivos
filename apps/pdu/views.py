from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import subprocess
from . import controller
from apps.modelo.controller import listar_modelos
from apps.ciudad.controller import listar_ciudad
from apps.regional.controller import listar_regionales, asignar_regional
from apps.ubicacion.controller import listar_tipos, crear_ubicacion, eliminar_ubicacion

# Create your views here.
def vista_pdu(request):
    return render(request, "pdu/pdu.html")

@login_required
def listado_pdu(request):
    marca = request.GET.get('marca', '').strip()
    nfb = request.GET.get('nfb', '').strip()
    serie = request.GET.get('serie', '').strip()
    admin = request.GET.get('admin', '').strip()

    pdus = controller.listado_pdu()

    filtrados = []
    for pdu in pdus:
        # Obtener valores seguros (evita errores si son None)
        nombre_marca = getattr(getattr(pdu.modelo, 'marca', None), 'nombre', '') or ''
        nombre_modelo = getattr(pdu.modelo, 'nombre', '') or ''
        nfb_valor = getattr(pdu, 'nfb', '') or ''
        serie_valor = getattr(pdu, 'serie', '') or ''
        admin_valor = getattr(pdu, 'admin', False)

        # Verificar coincidencias
        if marca and marca.lower() not in (nombre_marca.lower() + ' ' + nombre_modelo.lower()):
            continue
        if nfb and nfb.lower() not in nfb_valor.lower():
            continue
        if serie and serie.lower() not in serie_valor.lower():
            continue
        if admin in ['True', 'False'] and admin_valor != (admin == 'True'):
            continue

        filtrados.append(pdu)

    pdus = filtrados
    
    items_por_pagina = int(request.GET.get('items', 10))
    paginator = Paginator(pdus, items_por_pagina)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    datos_mostrados = page_obj.end_index() - page_obj.start_index() + 1
    total_datos = paginator.count
    
    # Ventana de páginas
    max_paginas = 5
    total_paginas = paginator.num_pages
    current = page_obj.number

    half_window = max_paginas // 2
    start = max(current - half_window, 1)
    end = min(start + max_paginas - 1, total_paginas)

    # Ajuste si llegamos al final
    start = max(end - max_paginas + 1, 1)

    rango_paginas = range(start, end + 1)
    
    datos = {
        'pdus': page_obj.object_list,  # muestra solo los del rango actual
        'page_obj': page_obj,
        'items': items_por_pagina,
        'rango_paginas': rango_paginas,
        'datos_mostrados': datos_mostrados,
        'total_datos': total_datos,
        'modelos': listar_modelos(),
        'ciudades': listar_ciudad(),
        'tipos': listar_tipos(),
        'marca': marca,
        'nfb': nfb,
        'serie': serie,
        'admin': admin,
    }

    # Si viene por AJAX devolvemos solo el cuerpo de la tabla
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'pdu/listado_pdu.html', datos)

    # Caso normal: render completo
    return render(request, "pdu/listado_pdu.html", datos)

@login_required
def agregar_pdu(request):
    if request.method == "POST":
        try:
            # Recuperar datos del formulario
            nombre_ubicacion = request.POST.get("nombre").title()
            tipo = request.POST.get("tipo").title()
            ciudad_id = request.POST.get("ciudad")
            admin = request.POST.get("admin") == "on"
            
            # Validaciones básicas
            if not nombre_ubicacion or not tipo or not ciudad_id:
                messages.error(request, "Todos los campos obligatorios deben completarse.")
                raise ValueError("Campos obligatorios incompletos.")

            # Campos opcionales (si es admin)
            modelo_id = request.POST.get("modelo") if admin else None
            nfb = request.POST.get("nfb") if admin else None
            serie = request.POST.get("serie").upper() if admin else None
            ip = request.POST.get("ip") if admin else None
            usuario = request.POST.get("usuario") if admin else None
            clave = request.POST.get("clave") if admin else None

            if admin:
                # Al menos un campo clave debe estar lleno
                if not modelo_id:
                    messages.error(request, "Debe seleccionar un modelo.")
                    raise ValueError("Modelo no seleccionado.")
                
                #Validad duplicados
                duplicado = controller.validar_dublicados(nfb, serie, ip)
                if controller.mensaje_error_duplicado(request, duplicado, nfb, serie, ip):
                    raise ValueError("Duplicado detectado.")
                
            ubicacion = crear_ubicacion(tipo=tipo, nombre=nombre_ubicacion, ciudad_id=ciudad_id)
            regional_id = asignar_regional(tipo=tipo, ciudad_id=int(ciudad_id))
            
            # Condicional para crear PDU
            if admin:
                controller.crear_pdu_adm(modelo_id=modelo_id, ubicacion_id=ubicacion.id, regional_id=regional_id, nfb=nfb, serie=serie, ip=ip, usuario=usuario, clave=clave)
            else:
                controller.crear_pdu_no_adm(ubicacion_id=ubicacion.id, regional_id=regional_id)

            messages.success(request, "✅ Agregado exitosamente.")
            return redirect("pdu")  # redirige a la lista de PDUs
        except ValueError:
            # Se manejan arriba con mensajes específicos
            pass
        except Exception as e:
            messages.error(request, f"Ocurrió un error al agregar el dispositivo: {e}")
        
    # Si es GET, cargamos los datos usando los controladores
    modelos = listar_modelos()
    ciudades = listar_ciudad()
    regionales = listar_regionales()
    tipos = listar_tipos()

    data = {
        "modelos": modelos,
        "ciudades": ciudades,
        "regionales": regionales,
        "tipos": tipos,
    }
    return render(request, "pdu/agregar_pdu.html", data)

@login_required
def editar_pdu(request, pdu_id):
    pdu = controller.obtener_pdu(pdu_id)
    if not pdu:
        messages.error(request, "El PDU no existe.")
        return redirect("pdu")

    if request.method == "POST":
        try:
            nombre_ubicacion = request.POST.get("ubicacion").title()
            tipo = request.POST.get("tipo").title()
            ciudad_id = request.POST.get("ciudad")
            admin = request.POST.get("admin") == "True"

            modelo_id = request.POST.get("modelo") if admin else None
            nfb = request.POST.get("nfb") if admin else None
            serie = request.POST.get("serie").upper() if admin else None
            ip = request.POST.get("ip") if admin else None
            usuario = request.POST.get("usuario") if admin else None
            clave = request.POST.get("clave") if admin else None
            
            if admin:
                # if not modelo_id:
                #     messages.error(request, "Debe seleccionar un modelo.")
                #     raise ValueError("Modelo no seleccionado.")

                duplicado = controller.validar_dublicados_editar(pdu_id, nfb, serie, ip)
                if duplicado:
                    controller.mensaje_error_duplicado(request, duplicado, nfb, serie, ip)
                    raise ValueError("Duplicado detectado.")

            # Actualizar ubicación
            pdu.ubicacion.tipo = tipo
            pdu.ubicacion.nombre = nombre_ubicacion
            pdu.ubicacion.ciudad_id = ciudad_id
            pdu.ubicacion.save()

            regional_id = asignar_regional(tipo=tipo, ciudad_id=int(ciudad_id))
            pdu.regional_id = regional_id

            if admin:
                pdu.modelo_id = modelo_id if modelo_id else None
                pdu.nfb = nfb or None
                pdu.serie = serie or None
                pdu.ip = ip or None
                pdu.usuario = usuario or None
                pdu.clave = clave or None
                pdu.admin = True
            else:
                pdu.modelo = None
                pdu.nfb = None
                pdu.serie = None
                pdu.ip = None
                pdu.usuario = None
                pdu.clave = None
                pdu.admin = False
            
            pdu.save()
            messages.success(request, "✅ Actualizado correctamente.")
            return redirect("pdu")

        except ValueError:
            # Mantener los parámetros actuales de la lista
            referer = request.META.get("HTTP_REFERER", "/pdu/")  # URL previa o lista por defecto
            url_parts = referer.split("?")
            base_url = url_parts[0]
            query = url_parts[1] if len(url_parts) > 1 else ""

            # Convertimos los parámetros actuales en un dict
            from urllib.parse import parse_qs, urlencode
            query_dict = parse_qs(query)
            query_dict["modal_abierto"] = [pdu_id]  # forzamos el modal

            nueva_url = f"{base_url}?{urlencode(query_dict, doseq=True)}"
            return redirect(nueva_url)

        except Exception as e:
            messages.error(request, f"Ocurrió un error al actualizar: {e}")
            return redirect("pdu")
    # ✅ Si llega aquí, es un GET → mostrar formulario
    return render(request, "pdu/editar_pdu.html", {"pdu": pdu})
            
@login_required
def eliminar_pdu(request, ubicacion_id):
    try:
        resultado = eliminar_ubicacion(ubicacion_id)
        
        if resultado:
            messages.success(request, "Eliminado correctamente")
        else:
            messages.warning(request, "Error al eliminar")
    except Exception as e:
        messages.error(f"Error al eliminar")
        
    return redirect('pdu')

@require_GET
def ping_pdu(request, ip):
    print(f"IP: {ip}")
    """
    Hace ping ICMP a la IP y devuelve JSON con:
    - activa: True/False
    - tiempo_ms: tiempo de respuesta aproximado en milisegundos
    """
    try:
        # Para Linux (contenedor)
        output = subprocess.run(
            ["ping", "-c", "1", ip],
            capture_output=True,
            text=True
        )

        if output.returncode == 0:
            # Extraer tiempo de respuesta de la salida
            # Ejemplo de línea: "64 bytes from 192.168.1.50: icmp_seq=1 ttl=64 time=1.23 ms"
            line = output.stdout.splitlines()[1]  # segunda línea
            time_part = [p for p in line.split() if "time=" in p][0]
            tiempo_ms = time_part.split("=")[1]  # "1.23"
            tiempo_ms = float(tiempo_ms)
            return JsonResponse({"activa": True, "tiempo_ms": tiempo_ms})
        else:
            return JsonResponse({"activa": False, "tiempo_ms": None})
    except Exception:
        return JsonResponse({"activa": False, "tiempo_ms": None})