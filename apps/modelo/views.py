from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .controller import listar_modelos, crear_modelo, eliminar_modelo_controller, actualizar_modelo, obtener_modelo, modelo_existe, modelo_existe_en_marca, modelo_marca_existe, modelo_existe_global
from apps.marca.controller import listar_marcas, listar_dispositivos
from apps.modelo.models import Modelo

# Create your views here.
@login_required
def listado_modelo(request):
    nombre_marca = request.GET.get('nombre', '')
    nombre_modelo = request.GET.get('modelo', '')

    modelos = listar_modelos(nombre_marca=nombre_marca, nombre_modelo=nombre_modelo)
    marcas = listar_marcas(nombre=nombre_marca)
    dispositivos = listar_dispositivos()
    abrir_modal_marca = request.session.pop('abrir_modal_marca', False)
    abrir_modal_modelo = request.session.pop('abrir_modal_modelo', False)
    abrir_modal_editar = request.session.pop('abrir_modal_editar', False)

    data = {
        'dispositivos': dispositivos,
        'modelos': modelos,
        'marcas': marcas,
        'nombre_buscar': nombre_marca,
        'modelo_buscar': nombre_modelo,
        'abrir_modal_marca': abrir_modal_marca,
        'abrir_modal_modelo': abrir_modal_modelo,
        'abrir_modal_editar': abrir_modal_editar,
    }
    return render(request, 'marca/list_marca.html', data)

@login_required
def agregar_modelo(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        marca_id = request.POST.get('marca')

        if not nombre or not marca_id:
            messages.warning(request, 'Debe completar todos los campos.', extra_tags="warning")
            return redirect('listado_marca')

        if modelo_existe(nombre, marca_id):
            messages.error(request, 'Ya existe ese modelo para esa marca.', extra_tags="danger")
            request.session['abrir_modal_modelo'] = True
            return redirect('listado_marca')
        
        if modelo_existe_global(nombre):
            messages.error(request, 'Ya existe ese modelo en otra marca.', extra_tags="danger")
            request.session['abrir_modal_modelo'] = True
            return redirect('listado_marca')

        crear_modelo(nombre, marca_id)
        messages.success(request, 'Modelo agregado correctamente.', extra_tags="success")
        return redirect('listado_marca')

    return redirect('listado_marca')
    
def editar_modelo(request, modelo_id):
    if request.method == 'POST':
        modelo = obtener_modelo(modelo_id)
        nombre = request.POST.get('nombre')
        marca_id = request.POST.get('marca')

        if not nombre or not marca_id:
            messages.warning(request, 'Debe completar todos los campos.', extra_tags="warning")
            request.session['abrir_modal_editar'] = modelo_id
            return redirect('listado_marca')

        if modelo_marca_existe(nombre, marca_id, modelo_id):
            messages.error(request, 'Ya existe ese modelo con esa marca.', extra_tags="danger")
            request.session['abrir_modal_editar'] = modelo_id
            return redirect('listado_marca')

        if modelo_existe_en_marca(nombre, modelo_id):
            messages.error(request, 'Ya existe ese modelo en otra marca.', extra_tags="danger")
            request.session['abrir_modal_editar'] = modelo_id
            return redirect('listado_marca')

        actualizar_modelo(modelo.id, nombre, marca_id)
        messages.success(request, 'Modelo actualizado correctamente.', extra_tags="success")
        return redirect('listado_marca')

    return redirect('listado_marca')

    
@login_required
def eliminar_modelo(request, modelo_id):
    if request.method == 'POST':
        eliminar_modelo_controller(modelo_id)
        return redirect('listado_marca')
    return redirect('listado_marca')