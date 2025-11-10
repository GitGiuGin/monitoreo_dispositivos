from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .controller import crear_marca, marca_existe

@login_required
def agregar_marca(request):
    if request.method == 'POST':
        dispositivo = request.POST.get('dispositivo').upper()
        nombre = request.POST.get('nombre').upper()

        if not dispositivo or not nombre:
            messages.warning(request, 'Debe completar todos los campos.', extra_tags="warning")
            return redirect('listado_marca')

        if marca_existe(dispositivo, nombre):
            messages.error(request, 'Ya existe una marca con ese nombre para este dispositivo.', extra_tags="danger")
            request.session['abrir_modal_marca'] = True
            return redirect('listado_marca')

        crear_marca(dispositivo, nombre)
        messages.success(request, 'Marca agregada correctamente.', extra_tags="success")
        return redirect('listado_marca')

    return redirect('listado_marca')