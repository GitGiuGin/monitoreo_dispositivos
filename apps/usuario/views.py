from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from urllib.parse import parse_qs, urlencode
from django.contrib import messages
from apps.usuario.controller import obtener_usuarios, usuario_existe, nuevo_usuario, obtener_usuario_por_id, actualizar_usuario, reinicar_contraseña

User = get_user_model()

def vista_login(request):
    if request.method == "POST":
        usuario_input = request.POST.get("usuario")
        contraseña = request.POST.get("contraseña")

        try:
            user_obj = User.objects.get(usuario=usuario_input)
        except User.DoesNotExist:
            user_obj = None

        if user_obj and not user_obj.is_active:
            messages.error(request, "La cuenta está deshabilitada", extra_tags="danger")
        else:
            user = authenticate(request, username=usuario_input, password=contraseña)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Usuario o contraseña incorrectos", extra_tags="danger")

    return render(request, "registration/login.html")

@login_required
def desconectar(request):
    logout(request)
    return redirect('login')

def reconstruir_url(referer, modal=None):
    url_parts = referer.split("?")
    base_url = url_parts[0]
    query = url_parts[1] if len(url_parts) > 1 else ""
    query_dict = parse_qs(query)

    if modal:
        query_dict["modal_abierto"] = [modal]

    return f"{base_url}?{urlencode(query_dict, doseq=True)}" if query_dict else base_url

@login_required
def cambiar_contraseña(request):
    if request.method == "POST":
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        user = request.user

        referer = request.META.get("HTTP_REFERER", "/dashboard/")

        if not user.check_password(old_password):
            messages.error(request, "La contraseña actual es incorrecta.", extra_tags="danger")
            return redirect(reconstruir_url(referer, "cambiarPasswordModal"))

        if new_password1 != new_password2:
            messages.error(request, "Las nuevas contraseñas no coinciden.", extra_tags="danger")
            return redirect(reconstruir_url(referer, "cambiarPasswordModal"))

        user.set_password(new_password1)
        user.cambiar_password = False
        user.save()
        update_session_auth_hash(request, user)

        messages.success(request, "Contraseña cambiada correctamente.", extra_tags="success")
        return redirect(reconstruir_url(referer))

    return redirect('dashboard')

@login_required
def gestion_usuarios(request):
    roles_disponibles = request.user.puede_crear_roles()

    if request.user.id == 1:
        usuarios = obtener_usuarios()
    else:
        usuarios = obtener_usuarios().exclude(id=1)

    for u in usuarios:
        u.puede_ser_editado = request.user.puede_editar(u)

    context = {
        'usuarios': usuarios,
        'roles': roles_disponibles,
        'rol_actual': request.user.rol,
    }
    return render(request, "usuario/gestion_usuario.html", context)


@login_required
def crear_usuario(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contraseña = request.POST.get('contraseña')
        rol = request.POST.get('rol')

        if usuario_existe(usuario):
            messages.error(request, "❌ El nombre de usuario ya existe.", extra_tags="danger")
        else:
            nuevo_usuario(usuario, contraseña, rol)
            messages.success(request, "✅ Usuario creado exitosamente.", extra_tags="success")

    return redirect('gestion_usuario')

@login_required
def obtener_form_editar_usuario(request, usuario_id):
    usuario = obtener_usuario_por_id(usuario_id=usuario_id)
    return render(request, 'usuario/form_editar_usuario.html', {'usuario': usuario})

@login_required
def editar_usuario(request, usuario_id):
    usuario = obtener_usuario_por_id(usuario_id=usuario_id)

    if request.method == 'POST':
        nuevo_rol = request.POST.get('rol')
        nuevo_estado = request.POST.get('estado')
        usuario_actual = request.user

        roles_permitidos = usuario_actual.puede_crear_roles()
        if nuevo_rol not in roles_permitidos:
            messages.error(request, "❌ No tienes permisos para asignar ese rol.", extra_tags="danger")
            return redirect('gestion_usuario')

        actualizar_usuario(usuario, nuevo_rol, nuevo_estado)
        messages.success(request, "✅ Usuario actualizado correctamente.", extra_tags="success")
        return redirect('gestion_usuario')

    return redirect('gestion_usuario')

@login_required
def resert_password(request, usuario_id):
    usuario = obtener_usuario_por_id(usuario_id=usuario_id)
    reinicar_contraseña(usuario)
    messages.success(request, "✅ Contraseña reiniciada.", extra_tags="success")
    return redirect('gestion_usuario')