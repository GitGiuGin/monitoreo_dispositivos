from django.db.models import Case, When, IntegerField
from .models import Usuario

def obtener_usuarios():
    rol_ordering = Case(
        When(rol='ADMINISTRADOR', then=0),
        When(rol='SUPERVISOR', then=1),
        When(rol='TECNICO', then=2),
        When(rol='USUARIO', then=3),
        output_field=IntegerField(),
    )
    usuarios = Usuario.objects.all().order_by(rol_ordering, 'id')
    # Asignar nivel de rol a cada usuario para comparar en template
    ROLES_JERARQUIA = {'ADMINISTRADOR': 3, 'SUPERVISOR': 2, 'TECNICO': 1, 'USUARIO': 0}
    for u in usuarios:
        u.nivel_rol = ROLES_JERARQUIA.get(u.rol, -1)
    return usuarios

def obtener_usuario_por_id(usuario_id):
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        return usuario
    except Usuario.DoesNotExist:
        return None

def usuario_existe(usuario):
    existe = Usuario.objects.filter(usuario=usuario).exists()
    return existe

def nuevo_usuario(usuario, contraseña, rol):
    nuevo_usuario = Usuario.objects.create_user(usuario=usuario, contraseña=contraseña, rol=rol, cambiar_password=True )
    return nuevo_usuario

def actualizar_usuario(usuario, rol, estado):
    usuario.rol = rol
    usuario.is_active = int(estado)
    usuario.save()
    
def reinicar_contraseña(usuario):
    usuario.set_password("$intesi$.2025")
    usuario.cambiar_password = True
    usuario.save()