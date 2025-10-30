from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UsuarioManager(BaseUserManager):
    def create_user(self, usuario, contraseña, **extra_fields):
        if not usuario:
            raise ValueError("El usuario debe tener un nombre de usuario")
        user = self.model(usuario=usuario, **extra_fields)
        user.set_password(contraseña)
        user.save(using=self._db)
        return user

    def create_superuser(self, usuario, contraseña, **extra_fields):
        extra_fields.setdefault('rol', 'ADMINISTRADOR')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(usuario, contraseña, **extra_fields)
    
class Usuario(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ('ADMINISTRADOR', 'Administrador'),
        ('SUPERVISOR', 'Supervisor'),
        ('TECNICO', 'Técnico'),
        ('USUARIO', 'Usuario'),
    ]
    # nombres = models.CharField(max_length=100)
    # apellidos = models.CharField(max_length=100)
    usuario = models.CharField(max_length=30, unique=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='USUARIO')
    estado = models.BooleanField(default=True)
    cambiar_password = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # necesario para admin
    is_active = models.BooleanField(default=True)  # necesario para auth
    
    objects = UsuarioManager()

    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = ['nombres', 'apellidos']

    class Meta:
        verbose_name = ("Usuario")
        verbose_name_plural = ("Usuarios")

    def __str__(self):
        return f"{self.usuario}"
    
    # --- 🔒 Métodos de ayuda para jerarquía ---
    def puede_crear_roles(self):
        if self.rol == 'ADMINISTRADOR' and self.id == 1:
            return ['ADMINISTRADOR', 'SUPERVISOR', 'TECNICO', 'USUARIO']
        if self.rol == 'ADMINISTRADOR':
            return ['SUPERVISOR', 'TECNICO', 'USUARIO']
        if self.rol == 'SUPERVISOR':
            return ['TECNICO', 'USUARIO']
        return []

    def puede_editar(self, otro_usuario):
        jerarquia = {
            'ADMINISTRADOR': 3,
            'SUPERVISOR': 2,
            'TECNICO': 1,
            'USUARIO': 0,
        }

        # Admin principal (ID=1) puede editar a todos menos a sí mismo
        if self.rol == 'ADMINISTRADOR' and self.id == 1:
            return self.id != otro_usuario.id

        # Los demás: solo pueden editar roles inferiores
        return jerarquia.get(self.rol, -1) > jerarquia.get(otro_usuario.rol, -1)

